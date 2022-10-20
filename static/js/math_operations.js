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