# kma-collect

기상자료개방포털에서 제공하는 종관기상관측 데이터를 수집하는 파이썬 프로그램입니다.

## Usage

1. API key 발급

기상자료개방포털에서 본인의 API key를 발급받아야 합니다. https://data.kma.go.kr/api/selectApiList.do 에서 종관기상관측 일자료, 종관기상관측 시간자료를 활용신청 해주세요. API key를 발급받았다면 "api_key"라는 이름으로 한 줄짜리 텍스트파일을 생성합니다 (이 파일에는 확장자가 없습니다).

```
<YOUR API KEY>
```

예를 들어, API key가 `J/qiwnfionseawf/ineiufn39anilnuacq2u3fb2u0/fea0jkweB`라면 다음과 같이 만들면 됩니다.

```
J/qiwnfionseawf/ineiufn39anilnuacq2u3fb2u0/fea0jkweB
```

2. 입력 파일 생성

다음으로, 수집하려는 데이터에 맞게 입력 파일을 생성합니다. 이름은 "inputfile.json"으로 설정해야 합니다. 다음은 입력 파일 예시입니다.

```json
{
    "stn_id" : 131,
    "start_year" : 2017,
    "end_year" : 2018,
    "date_cd" : "DAY",

    "destination" : "weather_daily.csv",

    "features" : [
        "MAX_TA", "MIN_TA", "AVG_WS", "AVG_TCA", "AVG_TD", "SUM_GSR"
    ]
}
```

`stn_id`에는 관측지점번호, `date_cd`에는 일자료를 수집하려면 `"DAY"`, 시간자료를 수집하려면 `"HR"`를 입력합니다. `destination`에는 수집된 데이터를 저장할 파일 이름, `features`에는 수집하려는 기상특성들을 입력합니다. 기상특성은 [metadata.md](./metadata.md)를 참고해주세요.

3. 프로그램 실행

앞서 만들었던 api_key 파일과 inputfile.json 파일이 collect.py 파일과 같은 폴더에 있어야 합니다. 해당 디렉토리에서 다음과 같이 collect.py 코드를 실행시키면 data 폴더 내에 데이터 파일이 생성됩니다.

```
python collect.py
```
