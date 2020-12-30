# HooongKart

----

<img src="https://img.shields.io/badge/Python-3.8.2-blue">  <img src="https://img.shields.io/badge/Django-3.1.4-green">  <img src="https://img.shields.io/badge/PostgresQl-12.4-orange">  <img src="https://img.shields.io/badge/Bootstrap-5.0.0-informational">  <img src="https://img.shields.io/badge/Redis-6.0.9-orange">

<br>

## Introduction

 본 프로젝트는 카트라이더 전적 검색 서비스를 제 나름대로 클론 코딩을 해본 것입니다.

<div align="center">

<img width="300" alt="스크린샷 2020-12-30 오전 12 25 10" src="https://user-images.githubusercontent.com/37801041/103294609-87fa9300-4a35-11eb-89cc-a32d136cf7a1.png"><img width="300" alt="스크린샷 2020-12-30 오전 12 25 16" src="https://user-images.githubusercontent.com/37801041/103294613-89c45680-4a35-11eb-89e4-59739a823b49.png">

</div>

- 라이더명을 입력하여 해당 유저의 최근 10경기에 대한 정보 제공
- Redis를 사용해 각종 메타데이터를 캐싱하였음.
  - API에서 메타데이터(맵, 카트, 캐릭터 등..)를 해시값으로 제공하여 해당하는 해시값을 찾아야함.

- 쿠키를 사용해 최근 검색했던 닉네임을 최신순으로 보여줌.
