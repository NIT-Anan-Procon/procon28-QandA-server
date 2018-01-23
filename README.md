# QandA_server

社会実装プロジェクト：Q&A用サーバ
・消防署でアプリ使用者の位置情報を地図を見ながら119番通報に対応できる
・通報と別に問診データが送信されるので、ダブルチェックになって伝え漏れやミスを減らせる。さらにスピードアップが謀れる。

## Description

Q&Aアプリからの位置情報を受診し、マップにマーカーを表示する。Q＆Aアプリには固有のIDを割り当てる。
Q&Aアプリが問診を終えると問診情報を送信する。サーバは受け取った情報を地図上から確認できる。
Q&Aアプリ経由で119番通報をすると、地図上のマーカーが赤くなり音で知らせる。
サーバからボタン操作で必要な応急手当てを指示できる。Q&Aアプリで情報を取得して、指示通りの応急手当てをすぐに始められる。

## Installation

    $ git clone https://github.com/NIT-Anan-Procon/QandA_server.git
    $ cd QandA_server
    $ pip install -r requirements.txt

    データベースにPostgresqlを使用した。（導入方法は後日追記予定）

## Author

    樫福智哉 (1124064@st.anan-nct.ac.jp)

