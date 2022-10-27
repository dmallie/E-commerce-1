'use strict';
function vat(){
       // Take value of price from dom object
              var price = document.querySelector('.price');
             
       
       // multiply it with VAT rate 
              const vat_rate = 1.24; // 24% vat
       
              var inc_vat = vat_rate *  price;
              console.log(price);
       // post the result on the html file
              price.textContent = inc_vat;
}
       
//vat();
const plus 		= document.getElementsByName("button-plus");
const minus 	= document.getElementsByName("button-minus");
var quantity	= parseInt(document.getElementsByName("quantity").value, 10);
var item_price 	= document.querySelector("#price").innerHTML;
var item_vat 	= document.querySelector("#vat");

//console.log(plus);
function cal_price(){
// convert item_price to float value
	var price_float = parseFloat(item_price).toFixed(2);
// update price value in the html page
	var price = quantity*price_float;
	var vat_value = price * 1.24; // 24% vat rate
// then we'll format the string then  
	var update_value = price + '.00 $';
	//item_price.value = price;
	document.querySelector("#price").textContent = update_value;
	item_vat.textContent = vat_value.toFixed(2) + ' $ inc. vat'
// convert quantity to int value 
}

function increment(){
	quantity = isNaN(quantity) ? 0: quantity;
	quantity++;
	document.getElementsByName('quantity').value = quantity;
	cal_price();
	console.log(quantity);
}
/* plus[1].addEventListener('click', function(e){
	e.preventDefault();
	
}); */
plus.forEach(el => el.addEventListener("click", increment));
minus.addEventListener('click', function(e){
	e.preventDefault();
	quantity = isNaN(quantity) ? 0: quantity;
	if(quantity-- <= 0){
		quantity = 0;
	}
	document.getElementsByName('quantity').value = quantity;
	cal_price();
	//console.log(quantity);
});
