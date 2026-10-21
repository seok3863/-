import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D 축구 챌린지",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ 3D 축구 챌린지")
st.caption("메시 vs 호날두 · 보통 난이도 · 3인칭 축구")

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
    <span class="team" style="color:#65c9ff">MESSI · YOU</span>
    <span id="score">0 - 0</span>
    <span class="team" style="color:#ff8585">RONALDO · AI</span>
  </div>
  <div id="clock">90</div>
  <div id="status">WASD 이동 · SPACE 슛 · SHIFT 달리기</div>
  <div id="message">경기 시작!</div>
  <div id="help">
    <b>조작법</b><br>t
