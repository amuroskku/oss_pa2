# 5점/10점 짜리 프로젝트

# 구현 목표
###  본 프로젝트는 1982년 발매된 "소코반(そうこばん)" 게임이 목적이며, 모든 구멍에 모든 상자를 밀어넣어 퍼즐을 클리어 하는 것이 게임의 목표입니다. 모든 구멍이 채워질 경우 승리합니다.

# 구현 기능

* pygame, box2d 기반 게임 board(환경) 구현
* 키보드 입력으로 과일 조준 기능
* 동일 과일이 충돌 시 합쳐지는 기능

# Reference
[1] https://github.com/pygame/pygame "pygame"

# 지원 Operating Systems 및 실행 방법

## 지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :o:  |
| Linux  | :x: |
|MacOS  | :x:  |

## 실행 방법
### Windows

1. python3.12를 설치한다

2. powershell 창에서 아래 pip3 library를 설치

```
pip3 install pygame
```

3. 재부팅 이후 python3 main.py를 실행하면 게임 창이 뜨면서 실행됨.

### Linux

1. python3.12를 설치한다.

2. bash에 다음 명령어를 통해 pip3 library를 설치

```
pip3 install pygame
```

3. 재부팅 이후 python3 main.py를 실행하면 게임 창이 뜨면서 실행됨.


### MacOS

# 실행 예시
<span style="color:red">동영상 업로드 시 gif로 변환 후 링크를 삽입</span>
<span style="color:red">아래 홈페이지 참고 : https://onlydev.tistory.com/15 </span>

![oss](https://github.com/Evanthekim/oss_personal_project_phase1/assets/60501545/6ab0ee7f-2f39-4392-b7c6-4b9865216fd8)

# 코드 설명
## main.py
### class WatermelonGame
- Description : watermelon 게임을 수행하는 메인 클래스
  1. Def __init__ : 최초 게임을 초기화하는 단계, screen, world, contact_listener, watermelons(과일 body를 저장) 등을 초기화함.
  2. Def create_ground : 아래, 좌, 우의 벽(바운더리)를 생성하여 과일이 화면밖으로 나가는 것을 방지

### class ContactListener
- Description : 과일 간의 충돌을 탐지하는 ContactListener
  1. Def BeginContact() : 충돌 시 자동으로 실행되는 box2d 함수, 충돌 된 두 과일의 body를 to_destroy 어레이에 저장한다.
 

# TODO List
* 점수 계산하기
* 게임 끝나는 조건 추가하기
* 좌우 키를 누르고 있으면 빠르게 이동하기
* start, end, restart, menu 버튼 추가하기