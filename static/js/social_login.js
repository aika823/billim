var naver_id_login = new naver_id_login("WO73y3DTPypJ9B7qq56N", "http://billim.co.kr/login/social/naver/callback/");
var state = naver_id_login.getUniqState();
naver_id_login.setButton("white", 2,40);
naver_id_login.setDomain("http://billim.co.kr");
naver_id_login.setState(state);
naver_id_login.setPopup();
naver_id_login.init_naver_id_login();