건강보험심사평가원 데이터 수집&정제 방법

1. hira_final.py 프로그램을 실행 (데이터 수집), 결과로 hira_all_utf8.txt 파일이 생성됨

2. hira_clinic_pp.py 프로그램을 실행 (hira_all_urf8.txt 파일을 입력파일로 지정, 출력파일 이름은 디폴트로 'output_clinic.txt')

3. hira_clinic_split_print.py 프로그램을 실행 (단계 2에서 지정한 출력파일을 단계 3의 입력파일로 지정), 결과로 30101_대학병원.txt ~ 30503_한약국한약방.txt 파일이 생성됨

주) 별도로 제공하는 myutil.py 프로그램이 위치한 디렉토리가 PATH 환경변수에 포함되어 있어야 한다.
