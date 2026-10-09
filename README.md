# 트윈 의존성 영향 분석기

장비·센서·서비스 의존 그래프에서 장애의 downstream 영향 범위, 순환 참조, 핵심 단절 지점을 계산합니다.

## 핵심 기능

간선 방향을 provider→consumer로 고정하고 최단 영향 거리와 downstream 수를 함께 계산합니다. 알람 라우팅·재학습 순서·XR 상태 마스킹에 활용할 수 있습니다.

## 설치·실행

Python 3.10 이상, 외부 패키지·유료 API·장비 연결이 필요 없습니다.

~~~bash
git clone https://github.com/MetaSonGi/twin-dependency-impact-analyzer.git
cd twin-dependency-impact-analyzer
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
~~~

example-report.html 또는 result.html을 브라우저에서 열 수 있습니다. CDN과 서버 없이 동작하며 문자열은 HTML escape됩니다.

## 입출력 예제

[sample-input.json](sample-input.json), [example-output.json](example-output.json), [example-report.html](example-report.html)을 포함합니다.

~~~json
{
  "nodes": [
    {
      "id": "sensor-temp",
      "kind": "sensor"
    },
    {
      "id": "plc-1",
      "kind": "controller"
    },
    {
      "id": "twin-api",
      "kind": "service"
    },
    {
      "id": "xr-view",
      "kind": "consumer"
    },
    {
      "id": "alert",
      "kind": "consumer"
    }
  ],
  "edges": [
    {
      "from": "sensor-temp",
      "to": "plc-1"
    },
    {
      "from": "plc-1",
      "to": "twin-api"
    },
    {
      "from": "twin-api",
      "to": "xr-view"
    },
    {
      "from": "twin-api",
      "to": "alert"
    }
  ],
  "failures": [
    "sensor-temp",
    "twin-api"
  ]
}
~~~

출력 미리보기:

~~~text
{
  "impacts": [
    {
      "failure": "sensor-temp",
      "affected": [
        {
          "id": "sensor-temp",
          "distance": 0,
          "kind": "sensor"
        },
        {
          "id": "plc-1",
          "distance": 1,
          "kind": "controller"
        },
        {
          "id": "twin-api",
          "distance": 2,
          "kind": "service"
        },
        {
          "id": "alert",
          "distance": 3,
          "kind": "consumer"
        },
        {
          "id": "xr-view",
          "distance": 3,
          "kind": "consumer"
        }
      ]
    },
    {
      "failure": "twin-api",
      "affected": [
        {
          "id": "twin-api",
          "distance": 0,
          "kind": "service"
        },
        {
          "id": "alert",
          "distance": 1,
          "kind": "consumer"
        },
        {
          "id": "xr-view",
       
... 전체는 example-output.json 참조
~~~

## 설계 판단

간선 방향을 provider→consumer로 고정하고 최단 영향 거리와 downstream 수를 함께 계산합니다. 알람 라우팅·재학습 순서·XR 상태 마스킹에 활용할 수 있습니다. JSON 입출력으로 Python 작업 큐, Nest.js 자동화, XR/WebGL 모니터링 앞단에 연결할 수 있습니다. 실제 장비 상태는 변경하지 않습니다.

## 한계

확률적 고장, 복구 시간, AND/OR 종속성, 용량·중복 경로 신뢰도는 포함하지 않습니다. 가상의 경력, 논문 성능, 모델 재현, 실물 제조 검증을 주장하지 않습니다.

## 검증·근거

정상·경계·오류 테스트 4개를 실행했습니다. [VALIDATION.txt](VALIDATION.txt)와 [TRENDS.md](TRENDS.md)에 결과와 근거를 구분했습니다.

실행 기준일: 2026-10-10 (Asia/Seoul). 기존 저장소를 수정하지 않은 독립 프로그램입니다.
