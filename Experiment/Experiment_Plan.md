## Keyword
Queue, ETA, Priority, Distribute-Inference

ETA, Priority를 기반으로 Queue에 있는 데이터 처리 중간 처리시 Distribute-Inference
구현와 이론이 너무 복잡함..

Priority를 배제할 경우 가장 앞차가 사고날 활률이 높아짐 (99%이상)
따라서 단순화해야 할 경우 ETA 배제
개인적으로 Distribute-Inference는 필히 적용해야 된다고 생각
Distribute-Inference를 어떻게 하면 효과적으로 상황을 만들 수 있을까
아니면 Distribute-Inference를 앞 쪽 추론만 하는 것 -> 뒤쪽만 추론할 경우 구현 매우 복잡

## 실험 진행 
로컬 추론이 성능 제약될 경우 원격으로 변경
### 라인트레이서 구현
### 추종 로봇 구현
### 멀티 추종 로봇 구현

## 실험 내용
다양한 알고리즘 & 기법을 통해 완주가 가능한가
### 실험 기법
1. Full local
2. Half local, remote
3. Full remote

### 실험 맵
...
