


























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


⋮⋮⋮⋮⋮⋮⋮⋮
