function adjustAdults(value) {
  const adultsInput = document.getElementById("adults");
  const currentValue = parseInt(adultsInput.value, 10);
  if (currentValue + value >= 1) {
      adultsInput.value = currentValue + value;
  }
}

function selectTab(tab) {
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(t => t.classList.remove('active'));
  document.querySelector(`.tab:nth-child(${{
      oneWay: 1,
      roundTrip: 2,
      multiCity: 3
  }[tab]})`).classList.add('active');
}
