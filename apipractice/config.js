// KRX 주식시세정보 API 설정
// 공공데이터포털에서 발급받은 인증키
const CONFIG = {
    KRX_API_KEY: 'b6bb9c715523217634ed937f9007068217cdc3eff369d301787086b81def1493',
    BASE_URL: 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService'
};

// Node.js 환경에서 사용할 경우
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}


