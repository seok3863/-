import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D 축구 챌린지",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ 3D 축구 챌린지")
st.caption("나 vs AI · 보통 난이도 · 3인칭 축구")

st.markdown(
    """
    **조작법**
    - `W A S D` 또는 방향키: 이동
    - `Space`: 슛
    - `Shift`: 달리기
    - `R`: 경기 재시작
    - 게임 화면을 한 번 클릭한 다음 조작하세요.
    """
)

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; }
body {
  margin: 0;
  overflow: hidden;
  font-family: Arial, sans-serif;
  background: #172b20;
  color: white;
}
#game { width: 100%; height: 680px; position: relative; overflow: hidden; }
canvas { display: block; width: 100%; height: 100%; outline: none; }
#hud {
  position: absolute; top: 12px; left: 50%;
  transform: translateX(-50%);
  display: flex; align-items: center; gap: 15px;
  background: rgba(8,20,15,.88);
  border: 1px solid rgba(255,255,255,.3);
  border-radius: 14px; padding: 10px 20px;
  white-space: nowrap; z-index: 2;
}
.team { font-size: 13px; font-weight: bold; }
#score { font-size: 27px; font-weight: 900; letter-spacing: 4px; }
#clock {
  position: absolute; top: 78px; left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,.65); border-radius: 8px;
  padding: 6px 14px; font-weight: bold; z-index: 2;
}
#help {
  position: absolute; left: 12px; bottom: 12px;
  background: rgba(0,0,0,.65); border-radius: 10px;
  padding: 10px 12px; font-size: 12px; line-height: 1.7;
  z-index: 2;
}
#message {
  position: absolute; top: 38%; left: 50%;
  transform: translate(-50%,-50%);
  font-size: clamp(26px,5vw,48px); font-weight: 900;
  color: #ffe66d; text-shadow: 0 3px 10px #000;
  text-align: center; pointer-events: none; z-index: 3;
}
#restart {
  position: absolute; bottom: 12px; right: 12px; z-index: 3;
  border: none; border-radius: 10px; padding: 10px 15px;
  background: #f7d44a; color: #18261c; font-weight: bold;
  cursor: pointer;
}
#status {
  position: absolute; top: 112px; left: 50%;
  transform: translateX(-50%); font-size: 12px;
  background: rgba(0,0,0,.45); padding: 5px 9px;
  border-radius: 6px; z-index: 2; white-space: nowrap;
}
</style>
</head>
<body>
<div id="game" tabindex="0">
  <div id="hud">
    <span class="team" style="color:#65c9ff">BLUE · YOU</span>
    <span id="score">0 - 0</span>
    <span class="team" style="color:#ff8585">RED · AI</span>
  </div>
  <div id="clock">90</div>
  <div id="status">WASD 이동 · SPACE 슛 · SHIFT 달리기</div>
  <div id="message">경기 시작!</div>
  <div id="help">
    <b>조작법</b><br>
    WASD / 방향키 : 이동<br>
    SPACE : 슛<br>
    SHIFT : 달리기<br>
    R : 다시 시작
  </div>
  <button id="restart">↻ 다시 시작</button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(() => {
const root = document.getElementById('game');
const scoreEl = document.getElementById('score');
const clockEl = document.getElementById('clock');
const messageEl = document.getElementById('message');
const statusEl = document.getElementById('status');

if (!window.THREE) {
  messageEl.textContent = '3D 엔진 로딩 실패';
  statusEl.textContent = '인터넷 연결을 확인한 뒤 페이지를 새로고침하세요.';
  return;
}

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9bd9ff);
scene.fog = new THREE.Fog(0x9bd9ff, 55, 115);

const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 180);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.7));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputEncoding = THREE.sRGBEncoding;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe5f6ff, 0x47633d, 2.0));
const sun = new THREE.DirectionalLight(0xffffff, 2.0);
sun.position.set(-15, 28, 12);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.left = -35;
sun.shadow.camera.right = 35;
sun.shadow.camera.top = 35;
sun.shadow.camera.bottom = -35;
scene.add(sun);

const W = 34, L = 54;
const mat = (color, roughness=0.8) =>
  new THREE.MeshStandardMaterial({color, roughness});

const grassMats = [mat(0x247c3b), mat(0x2b8841)];
const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(90,110),
  mat(0x356d3c)
);
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.12;
ground.receiveShadow = true;
scene.add(ground);

// 잔디 줄무늬
for (let i=0; i<10; i++) {
  const stripe = new THREE.Mesh(
    new THREE.PlaneGeometry(W, L/10),
    grassMats[i%2]
  );
  stripe.rotation.x = -Math.PI/2;
  stripe.position.set(0, -0.04, -L/2 + L/20 + i*L/10);
  stripe.receiveShadow = true;
  scene.add(stripe);
}

const lineMat = new THREE.MeshBasicMaterial({color:0xffffff});
function line(x1,z1,x2,z2,y=0.035) {
  const dx=x2-x1, dz=z2-z1;
  const mesh = new THREE.Mesh(
    new THREE.PlaneGeometry(Math.hypot(dx,dz),0.13),lineMat
  );
  mesh.rotation.x=-Math.PI/2;
  mesh.rotation.z=-Math.atan2(dz,dx);
  mesh.position.set((x1+x2)/2,y,(z1+z2)/2);
  scene.add(mesh);
}
line(-W/2,-L/2,W/2,-L/2);
line(-W/2,L/2,W/2,L/2);
line(-W/2,-L/2,-W/2,L/2);
line(W/2,-L/2,W/2,L/2);
line(-W/2,0,W/2,0);

const circle = new THREE.Mesh(
  new THREE.RingGeometry(5.9,6.04,64),
  new THREE.MeshBasicMaterial({color:0xffffff,side:THREE.DoubleSide})
);
circle.rotation.x=-Math.PI/2;
circle.position.y=0.04;
scene.add(circle);

function box(w,h,d,material,x,y,z) {
  const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
  m.position.set(x,y,z);
  m.castShadow=true;
  m.receiveShadow=true;
  scene.add(m);
  return m;
}

// 페널티 박스와 골 에어리어
for (const sign of [-1,1]) {
  const z=sign*L/2;
  const edge=z-sign*8;
  line(-10,edge,10,edge);
  line(-10,z,-10,edge);
  line(10,z,10,edge);

  const smallEdge=z-sign*3.2;
  line(-5.2,smallEdge,5.2,smallEdge);
  line(-5.2,z,-5.2,smallEdge);
  line(5.2,z,5.2,smallEdge);

  const goalZ=z+sign*1.3;
  const postM=mat(0xf4f5f6,0.35);
  const goalW=10, goalH=3.3;
  box(0.22,goalH,0.22,postM,-goalW/2,goalH/2,goalZ);
  box(0.22,goalH,0.22,postM,goalW/2,goalH/2,goalZ);
  box(goalW,0.22,0.22,postM,0,goalH,goalZ);
  const netMat = new THREE.MeshBasicMaterial({
    color:0xffffff,wireframe:true,transparent:true,opacity:.18
  });
  const net=new THREE.Mesh(new THREE.BoxGeometry(goalW,goalH,2.6),netMat);
  net.position.set(0,goalH/2,z+sign*1.3);
  scene.add(net);
}

// 관중석 느낌의 단순한 외곽 구조
const standMat=mat(0x43566b);
box(42,1.8,3,standMat,0,0.9,-L/2-4);
box(42,1.8,3,standMat,0,0.9,L/2+4);
box(3,1.8,65,standMat,-W/2-4,0.9,0);
box(3,1.8,65,standMat,W/2+4,0.9,0);

function makePlayer(color, shortsColor, x, z) {
  const group=new THREE.Group();
  const jersey=mat(color,0.65);
  const shorts=mat(shortsColor,0.8);
  const skin=mat(0xe8b58b,0.8);
  const dark=mat(0x20252c,0.85);

  const torso=new THREE.Mesh(
    new THREE.CapsuleGeometry(0.55,0.9,4,8),jersey
  );
  torso.position.y=1.75;
  torso.castShadow=true;
  group.add(torso);

  const head=new THREE.Mesh(new THREE.SphereGeometry(0.34,16,12),skin);
  head.position.y=2.72;
  head.castShadow=true;
  group.add(head);

  const hair=new THREE.Mesh(new THREE.SphereGeometry(0.35,16,10,0,Math.PI*2,0,Math.PI/2),dark);
  hair.position.y=2.83;
  group.add(hair);

  const legL=new THREE.Mesh(new THREE.BoxGeometry(0.28,0.8,0.35),shorts);
  const legR=legL.clone();
  legL.position.set(-0.25,0.72,0);
  legR.position.set(0.25,0.72,0);
  legL.castShadow=legR.castShadow=true;
  group.add(legL,legR);

  const armL=new THREE.Mesh(new THREE.BoxGeometry(0.22,0.75,0.25),jersey);
  const armR=armL.clone();
  armL.position.set(-0.68,1.85,0);
  armR.position.set(0.68,1.85,0);
  group.add(armL,armR);

  group.position.set(x,0,z);
  scene.add(group);
  return {group,legL,legR,armL,armR,vx:0,vz:0};
}

const player=makePlayer(0x168de2,0x123b79,0,15);
const ai=makePlayer(0xe53945,0x8b1827,0,-13);

// 축구공
const ball=new THREE.Mesh(
  new THREE.SphereGeometry(0.48,24,18),
  mat(0xffffff,0.35)
);
ball.castShadow=true;
ball.position.set(0,0.48,0);
scene.add(ball);

// 공 표면의 검은 패치
const patchMat=mat(0x17191d,0.5);
for(let i=0;i<6;i++){
  const p=new THREE.Mesh(
    new THREE.CircleGeometry(0.16,5),
    patchMat
  );
  p.position.set(
    0.48*Math.sin(i*1.05),
    0.48*Math.cos(i*1.05),
    0.015
  );
  p.rotation.z=i*0.6;
  ball.add(p);
}

const keys={};
let blueScore=0,redScore=0;
let remaining=90, gameOver=false, goalPause=0, elapsed=0;
let ballV=new THREE.Vector3(0,0,0);
let kickCooldown=0, aiKickCooldown=0;
let lastTime=performance.now();
let toastTimer=0;

function updateScore(){
  scoreEl.textContent=blueScore+" - "+redScore;
  clockEl.textContent=Math.ceil(remaining);
}
function toast(text, duration=1.5){
  messageEl.textContent=text;
  toastTimer=duration;
}
function resetPositions(){
  player.group.position.set(0,0,15);
  ai.group.position.set(0,0,-13);
  player.vx=player.vz=ai.vx=ai.vz=0;
  ball.position.set(0,0.48,0);
  ballV.set(0,0,0);
}
function resetGame(){
  blueScore=0; redScore=0; remaining=90;
  gameOver=false; goalPause=0;
  kickCooldown=0; aiKickCooldown=0;
  resetPositions();
  toast("경기 시작!",1.4);
  updateScore();
}
function scoreGoal(who){
  if(gameOver || goalPause>0) return;
  if(who==="blue"){blueScore++;toast("⚽ GOAL! 득점!",1.8);}
  else {redScore++;toast("AI 득점!",1.8);}
  goalPause=1.65;
  updateScore();
  resetPositions();
}

function clampPlayer(p, blue){
  p.group.position.x=THREE.MathUtils.clamp(p.group.position.x,-W/2+1,W/2-1);
  p.group.position.z=THREE.MathUtils.clamp(p.group.position.z,-L/2+1,L/2-1);
}
function movePlayer(p, dx, dz, speed, dt, blue){
  const len=Math.hypot(dx,dz);
  if(len>0.001){dx/=len;dz/=len;}
  p.vx+=(dx*speed-p.vx)*Math.min(1,dt*9);
  p.vz+=(dz*speed-p.vz)*Math.min(1,dt*9);
  p.group.position.x+=p.vx*dt;
  p.group.position.z+=p.vz*dt;
  clampPlayer(p,blue);

  if(len>0.08){
    p.group.rotation.y=Math.atan2(dx,dz);
    const swing=Math.sin(elapsed*12)*0.48*Math.min(1,len);
    p.legL.rotation.x=swing;
    p.legR.rotation.x=-swing;
  } else {
    p.legL.rotation.x*=0.8;
    p.legR.rotation.x*=0.8;
  }
}
function distance2(a,b){
  return Math.hypot(a.x-b.x,a.z-b.z);
}
function shoot(p, towardZ, power, isAI=false){
  if((isAI?aiKickCooldown:kickCooldown)>0)return;
  const pos=p.group.position;
  const dx=ball.position.x-pos.x;
  const dz=ball.position.z-pos.z;
  if(Math.hypot(dx,dz)>3.1)return;

  // 슛은 선수의 진행 방향과 상대 골대 방향을 섞어 계산
  let aimX=ball.position.x*0.12;
  let aimZ=towardZ;
  const length=Math.hypot(aimX,aimZ)||1;
  aimX/=length;aimZ/=length;
  ballV.x=aimX*power;
  ballV.z=aimZ*power;
  ballV.y=power*0.17;
  if(isAI)aiKickCooldown=1.0;
  else kickCooldown=0.48;
}
function collideBallPlayer(p){
  const dx=ball.position.x-p.group.position.x;
  const dz=ball.position.z-p.group.position.z;
  const dist=Math.hypot(dx,dz);
  const minDist=1.35;
  if(dist<minDist && dist>0.001){
    const nx=dx/dist,nz=dz/dist;
    const overlap=minDist-dist;
    ball.position.x+=nx*overlap;
    ball.position.z+=nz*overlap;
    ballV.x+=nx*0.8+p.vx*0.25;
    ballV.z+=nz*0.8+p.vz*0.25;
  }
}

function update(dt){
  elapsed+=dt;
  if(toastTimer>0){
    toastTimer-=dt;
    if(toastTimer<=0)messageEl.textContent="";
  }
  kickCooldown=Math.max(0,kickCooldown-dt);
  aiKickCooldown=Math.max(0,aiKickCooldown-dt);

  if(gameOver)return;
  if(goalPause>0){
    goalPause-=dt;
    if(goalPause<=0)toast("");
    return;
  }

  remaining-=dt;
  if(remaining<=0){
    remaining=0;gameOver=true;
    toast(blueScore>redScore?"🏆 승리!":"경기 종료!",999);
    statusEl.textContent=blueScore===redScore
      ?"무승부! R 키로 다시 경기하세요."
      :blueScore>redScore
      ?"축하합니다! R 키로 다시 경기하세요."
      :"AI가 승리했습니다. R 키로 재도전하세요.";
    updateScore();
    return;
  }
  updateScore();

  let dx=0,dz=0;
  if(keys.KeyW||keys.ArrowUp)dz-=1;
  if(keys.KeyS||keys.ArrowDown)dz+=1;
  if(keys.KeyA||keys.ArrowLeft)dx-=1;
  if(keys.KeyD||keys.ArrowRight)dx+=1;

  const sprint=keys.ShiftLeft||keys.ShiftRight;
  movePlayer(player,dx,dz,sprint?10.0:7.0,dt,true);

  // AI: 공을 추적하고 공을 잡으면 반대편 골대를 향해 움직임
  const ap=ai.group.position;
  const bp=ball.position;
  let adx=bp.x-ap.x, adz=bp.z-ap.z;
  const ballDist=Math.hypot(adx,adz);
  let targetX=bp.x, targetZ=bp.z;

  if(ballDist<3.3){
    targetZ=bp.z+7.0;
    targetX=bp.x*0.6;
  } else {
    // 자기 진영을 너무 멀리 비우지 않도록 조절
    targetZ=Math.min(10,bp.z+2.0);
  }
  adx=targetX-ap.x;
  adz=targetZ-ap.z;
  const aimDist=Math.hypot(adx,adz);
  const aiSpeed=5.4;
  movePlayer(ai,adx,adz,aiSpeed,dt,false);

  if(ballDist<2.5){
    // AI가 골문을 바라보고 슛
    if(bp.z>1.5 && Math.random()<dt*1.0){
      shoot(ai,1,10.5,true);
    } else if(aiKickCooldown<=0 && Math.random()<dt*0.65){
      ballV.x+=(Math.random()-0.5)*2.4;
      ballV.z+=3.0;
    }
  }

  // 공과 선수 충돌
  collideBallPlayer(player);
  collideBallPlayer(ai);

  // 공 물리
  ballV.y-=16*dt;
  ball.position.x+=ballV.x*dt;
  ball.position.z+=ballV.z*dt;
  ball.position.y+=ballV.y*dt;

  if(ball.position.y<0.48){
    ball.position.y=0.48;
    if(ballV.y<0)ballV.y*=-0.34;
    ballV.x*=0.985;
    ballV.z*=0.985;
  }
  ball.rotation.x+=ballV.z*dt*0.6;
  ball.rotation.z-=ballV.x*dt*0.6;

  // 측면 아웃
  if(Math.abs(ball.position.x)>W/2-0.5){
    ball.position.x=Math.sign(ball.position.x)*(W/2-0.5);
    ballV.x*=-0.72;
  }

  // 골라인 및 골 판정
  if(ball.position.z < -L/2 || ball.position.z > L/2){
    const inGoal=Math.abs(ball.position.x)<5.0 && ball.position.y<3.5;
    if(inGoal){
      scoreGoal(ball.position.z<0?"blue":"red");
    }else{
      ball.position.z=Math.sign(ball.position.z)*(L/2-0.6);
      ballV.z*=-0.7;
    }
  }

  // 공이 지나치게 빨라지지 않도록 제한
  const horizontalSpeed=Math.hypot(ballV.x,ballV.z);
  if(horizontalSpeed>23){
    ballV.x*=23/horizontalSpeed;
    ballV.z*=23/horizontalSpeed;
  }
}

// 카메라: 선수 뒤쪽에서 공과 선수를 함께 보여줌
function updateCamera(dt){
  const p=player.group.position;
  const desired=new THREE.Vector3(p.x,11,p.z+15);
  camera.position.lerp(desired,1-Math.exp(-3.3*dt));
  const look=new THREE.Vector3(
    ball.position.x*0.35+p.x*0.65,
    0.6,
    ball.position.z*0.35+p.z*0.65-5
  );
  camera.lookAt(look);
}

function resize(){
  const w=root.clientWidth,h=root.clientHeight;
  if(!w||!h)return;
  renderer.setSize(w,h,false);
  camera.aspect=w/h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize',resize);
resize();

window.addEventListener('keydown',e=>{
  if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","Space"].includes(e.code)){
    e.preventDefault();
  }
  keys[e.code]=true;
  if(e.code==="Space"&&!e.repeat){
    shoot(player,-1,keys.ShiftLeft||keys.ShiftRight?17:13.5,false);
  }
  if(e.code==="KeyR"&&!e.repeat){
    resetGame();
    statusEl.textContent="WASD 이동 · SPACE 슛 · SHIFT 달리기";
  }
});
window.addEventListener('keyup',e=>{keys[e.code]=false;});
window.addEventListener('blur',()=>{Object.keys(keys).forEach(k=>keys[k]=false);});
document.getElementById('restart').addEventListener('click',()=>{
  resetGame();
  statusEl.textContent="WASD 이동 · SPACE 슛 · SHIFT 달리기";
  root.focus();
});
root.addEventListener('pointerdown',()=>root.focus());

resetGame();
function animate(now){
  requestAnimationFrame(animate);
  const dt=Math.min((now-lastTime)/1000,0.04);
  lastTime=now;
  update(dt);
  updateCamera(dt);
  renderer.render(scene,camera);
}
requestAnimationFrame(animate);
})();
</script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=False)

st.info(
    "팁: 게임 화면을 클릭한 뒤 이동하세요. "
    "공 가까이에서 스페이스바를 누르면 슛을 쏠 수 있습니다. "
    "경기 종료 후 R 키 또는 다시 시작 버튼을 누르세요."
)
