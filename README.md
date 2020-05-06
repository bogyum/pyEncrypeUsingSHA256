# pyEncrypeUsingSHA256
SHA256 Encryption project


## Ver. 0.0.1 :: prototype

### How to use

- python main script :: ./src/pyEncrypeUsingSHA256.py
- Using :: ./src/pyEncrypeUsingSHA256.py (키 변환 대상 파일명) (Salt 파일명) (키 변환 결과 파일명)

### 폴더 구조

- ./config :: 환경 설정 파일
- ./resource/data :: 키 변환 대상 파일
-- 키 변환 파일은 탭('\t')으로 값을 구분한다. 예를 들면, '홍길동 \t 801011 \t 1' 와 같이, 변환 대상 키 값인 이름, 생년월일, 성별 값을 탭을 기준으로 구분
- ./resource/salt :: Salt 텍스트 파일
- ./results :: 키 변환 결과 저장
