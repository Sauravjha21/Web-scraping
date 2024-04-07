let count = 0;

const countBtn = document.getElementById('count-btn');
const countDisplay = document.getElementById('count-display');

countBtn.addEventListener('click', () => {
  console.log('Button clicked');
  console.log('Count:', count);
  count++;
  countDisplay.innerText = `Count: ${count}`;
  countDisplay.style.color = count % 2 === 0 ? 'red' : 'blue';
});