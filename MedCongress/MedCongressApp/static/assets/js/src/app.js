document.addEventListener('DOMContentLoaded', e => {
    /* - Switch Languaje - */
    // languageTooglerSpanish.addEventListener('click', e => {
    //     if(!languageFlag.src.includes('bandera-mx.png')) languageFlag.src = languageFlag.src.replace('bandera-usa.png', 'bandera-mx.png');
    // });

    // languageTooglerEnglish.addEventListener('click', e => {
    //     if(!languageFlag.src.includes('bandera-usa.png')) languageFlag.src = languageFlag.src.replace('bandera-mx.png', 'bandera-usa.png');
    // });

    /* - Home Counter - */
    // Set the date we're counting down to

    if(typeof(counter) != "undefined") {
        const countDownDate = new Date(counter.getAttribute("countDate")).getTime();
        
        // Update the count down every 1 second
        const x = setInterval(function() {

        // Get today's date and time
        const now = new Date().getTime();

        // Find the distance between now and the count down date
        const distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        document.getElementById("counter").innerHTML = 
        `<div class="days">
            <strong>${days}</strong>
            <span>DIAS</span>
        </div>
        <div class="hours">
            <strong>${hours}</strong>
            <span>HORAS</span>
        </div>
        <div class="minutes">
            <strong>${minutes}</strong>
            <span>MINUTOS</span>
        </div>
        <div class="seconds">
            <strong>${seconds}</strong>
            <span>SEGUNDOS</span>
        </div>`;

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("counter").innerHTML = 
            `<div class="days">
                <strong>00</strong>
                <span>DIAS</span>
            </div>
            <div class="hours">
                <strong>00</strong>
                <span>HORAS</span>
            </div>
            <div class="minutes">
                <strong>00</strong>
                <span>MINUTOS</span>
            </div>
            <div class="seconds">
                <strong>00</strong>
                <span>SEGUNDOS</span>
            </div>`;
        }
        }, 1000);
    }

    /* Form Controller */
    (function () {
        'use strict'
      
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')
      
        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
          .forEach(function (form) {
            form.addEventListener('submit', function (event) {
              if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
              }
      
              event.preventDefault();
              event.stopPropagation();
              
              responseSending.classList.remove('d-none');

              form.classList.add('was-validated');
              const data = new FormData(form);
              fetch('./form-process.php', {
                method: 'POST',
                body: data
              })
              .then(function(response) {
                responseSending.classList.add('d-none');
                if(response.status === 200){
                    responseInvalid.classList.contains('d-none') || responseInvalid.classList.add('d-none');
                    responseValid.classList.remove('d-none');
                }else{
                    throw "Error en la llamada Ajax";
                }
             })
             .catch(function(err) {
                responseValid.classList.contains('d-none') || responseValid.classList.add('d-none');
                responseInvalid.classList.remove('d-none');
                responseInvalid.classList.add('d-block');
             });

            }, false);
          })
      })();

    /* Register Swith */

    if(typeof(registerCat) != "undefined") {
        registerCat.addEventListener('change', e => {
            if (e.target.value == 4 || e.target.value == 2) {
                especialidad.classList.remove('d-none');
                cedulaProfesional.classList.remove('d-none');
                otra.classList.add('d-none');
            } else if(e.target.value == 1) {
                otra.classList.remove('d-none');
            } else {
                especialidad.classList.add('d-none');
                cedulaProfesional.classList.add('d-none');
                otra.classList.add('d-none');
            }   
        });
    }

    /* Counter Up */

    const counterUpList = document.querySelectorAll('.counter-btns .up');
    counterUpList.forEach(counterUp => {
        counterUp.addEventListener('click', e => {
            const counterLabel = e.target.parentNode.parentNode.querySelector('.counterLabel');

            counterLabel.innerText = parseInt(counterLabel.innerText) + 1;
        });
    });

    const counterDownList = document.querySelectorAll('.counter-btns .down');
    counterDownList.forEach(counterDown => {
        counterDown.addEventListener('click', e => {
            const counterLabel = e.target.parentNode.parentNode.querySelector('.counterLabel');

            counterLabel.innerText = (counterLabel.innerText > 1) ? parseInt(counterLabel.innerText) - 1 : 1;
        });
    });

    /* Credit Cart Formating */

    var cleave = new Cleave('#card-number', {
        creditCard: true,
        onCreditCardTypeChanged: function (type) {
            // update UI ...
        }
    });
    
});