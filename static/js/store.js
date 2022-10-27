'use strict';
console.log("Store.html");
var plus_btn = document.querySelector("#button-plus");
var minus_btn = document.querySelector("#button-minus");
var quantity_input = document.querySelector("#quantity");

function increment(){
// bring quantity value in an integer and base 10 format
	var quantity = parseInt(quantity_input.value, 10);
// if value is null then take it as 0 otherwise don't change the value 	
	quantity = isNaN(quantity) ? 0 : quantity;
// increment the value of quantity by 1 and post it on quantity_input element;
	quantity_input.value = ++quantity;
}

function decrement(){
// bring quantity value in an integer and base 10 format
	var quantity = parseInt(quantity_input.value, 10);
// if value is null then take it as 0 otherwise don't change the value 	
	quantity = isNaN(quantity) ? 0 : quantity;
// decrease the value of quantity by 1 and post it on quantity_input element;
// if the value is less than 0 then stop decrementing
	if(--quantity > 0){
		quantity_input.value = quantity;
	}
	else{
		quantity_input.value = 0;
	}
}

plus_btn.addEventListener('click', increment);
minus_btn.addEventListener('click', decrement);