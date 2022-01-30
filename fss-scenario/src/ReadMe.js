import './ReadMe.css';

function ReadMe() {
  return (
    <>
      <h1>용어</h1>
      <section>
        <h3>1. LLP(Last Liquid Point, 최종관찰만기)</h3>
        <p>- 금리 데이터 쓸 때 마지막 테너를 어떤걸로 정할지 정하는거임</p>
        <p>- 부채 할인율 만들 때 LLP 이후의 금리는 직접적으로는 사용되지 않음</p>
        <p>- 자산 할인율 만들 때는 LLP 적용 안됨</p>
        <p>- 수렴시점(CP)은 MAX(LLP+30년, 60년)로 정함</p>
        <p>- KRW는 20년 적용 중</p>
      </section>
      <section>
        <h3>2. LTFR(Long Term Forward Rate, 장기선도금리)</h3>
        <p>- 선도금리가 수렴하는 지점</p>
        <p>- 금리를 Smith-Wilson으로 보간/보외할 때, 수렴시점(CP)에서 LTFR과의 오차가 1bp 이내가 되도록 수렴속도(α) 결정</p>
        <p>- 예전에는 UFR(Ultimate Forward Rate, 최종선도금리)라고 불리었다 명칭 바뀜</p>
        <p>- 통상 연단위로 표시 (Annually Compounded)</p>
        <p>- KRW는 4.95% 적용 중</p>
      </section>
    </>
  );
};

export default ReadMe;