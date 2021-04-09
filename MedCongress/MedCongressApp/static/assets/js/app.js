/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./assets/js/src/app.js":
/*!******************************!*\
  !*** ./assets/js/src/app.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

document.addEventListener('DOMContentLoaded', function (e) {
  /* - Switch Languaje - */
  languageTooglerSpanish.addEventListener('click', function (e) {
    if (!languageFlag.src.includes('bandera-mx.png')) languageFlag.src = languageFlag.src.replace('bandera-usa.png', 'bandera-mx.png');
  });
  languageTooglerEnglish.addEventListener('click', function (e) {
    if (!languageFlag.src.includes('bandera-usa.png')) languageFlag.src = languageFlag.src.replace('bandera-mx.png', 'bandera-usa.png');
  });
  /* - Home Counter - */
  // Set the date we're counting down to

  if (typeof counter != "undefined") {
    var countDownDate = new Date(counter.getAttribute("countDate")).getTime(); // Update the count down every 1 second

    var x = setInterval(function () {
      // Get today's date and time
      var now = new Date().getTime(); // Find the distance between now and the count down date

      var distance = countDownDate - now; // Time calculations for days, hours, minutes and seconds

      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor(distance % (1000 * 60 * 60 * 24) / (1000 * 60 * 60));
      var minutes = Math.floor(distance % (1000 * 60 * 60) / (1000 * 60));
      var seconds = Math.floor(distance % (1000 * 60) / 1000); // Display the result in the element with id="demo"

      document.getElementById("counter").innerHTML = "<div class=\"days\">\n            <strong>".concat(days, "</strong>\n            <span>DIAS</span>\n        </div>\n        <div class=\"hours\">\n            <strong>").concat(hours, "</strong>\n            <span>HORAS</span>\n        </div>\n        <div class=\"minutes\">\n            <strong>").concat(minutes, "</strong>\n            <span>MINUTOS</span>\n        </div>\n        <div class=\"seconds\">\n            <strong>").concat(seconds, "</strong>\n            <span>SEGUNDOS</span>\n        </div>"); // If the count down is finished, write some text

      if (distance < 0) {
        clearInterval(x);
        document.getElementById("counter").innerHTML = "<div class=\"days\">\n                <strong>00</strong>\n                <span>DIAS</span>\n            </div>\n            <div class=\"hours\">\n                <strong>00</strong>\n                <span>HORAS</span>\n            </div>\n            <div class=\"minutes\">\n                <strong>00</strong>\n                <span>MINUTOS</span>\n            </div>\n            <div class=\"seconds\">\n                <strong>00</strong>\n                <span>SEGUNDOS</span>\n            </div>";
      }
    }, 1000);
  }
  /* Form Controller */


  (function () {
    'use strict'; // Fetch all the forms we want to apply custom Bootstrap validation styles to

    var forms = document.querySelectorAll('.needs-validation'); // Loop over them and prevent submission

    Array.prototype.slice.call(forms).forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        event.preventDefault();
        event.stopPropagation();
        responseSending.classList.remove('d-none');
        form.classList.add('was-validated');
        var data = new FormData(form);
        fetch('./form-process.php', {
          method: 'POST',
          body: data
        }).then(function (response) {
          responseSending.classList.add('d-none');

          if (response.status === 200) {
            responseInvalid.classList.contains('d-none') || responseInvalid.classList.add('d-none');
            responseValid.classList.remove('d-none');
          } else {
            throw "Error en la llamada Ajax";
          }
        })["catch"](function (err) {
          responseValid.classList.contains('d-none') || responseValid.classList.add('d-none');
          responseInvalid.classList.remove('d-none');
          responseInvalid.classList.add('d-block');
        });
      }, false);
    });
  })();
  /* Register Swith */


  if (typeof registerCat != "undefined") {
    registerCat.addEventListener('change', function (e) {
      if (e.target.value == 4 || e.target.value == 2) {
        especialidad.classList.remove('d-none');
        cedulaProfesional.classList.remove('d-none');
        otra.classList.add('d-none');
      } else if (e.target.value == 1) {
        otra.classList.remove('d-none');
      } else {
        especialidad.classList.add('d-none');
        cedulaProfesional.classList.add('d-none');
        otra.classList.add('d-none');
      }
    });
  }
  /* Counter Up */


  var counterUpList = document.querySelectorAll('.counter-btns .up');
  counterUpList.forEach(function (counterUp) {
    counterUp.addEventListener('click', function (e) {
      var counterLabel = e.target.parentNode.parentNode.querySelector('.counterLabel');
      counterLabel.innerText = parseInt(counterLabel.innerText) + 1;
    });
  });
  var counterDownList = document.querySelectorAll('.counter-btns .down');
  counterDownList.forEach(function (counterDown) {
    counterDown.addEventListener('click', function (e) {
      var counterLabel = e.target.parentNode.parentNode.querySelector('.counterLabel');
      counterLabel.innerText = counterLabel.innerText > 1 ? parseInt(counterLabel.innerText) - 1 : 1;
    });
  });
  /* Credit Cart Formating */

  var cleave = new Cleave('#card-number', {
    creditCard: true,
    onCreditCardTypeChanged: function onCreditCardTypeChanged(type) {// update UI ...
    }
  });
});

/***/ }),

/***/ "./assets/scss/app.scss":
/*!******************************!*\
  !*** ./assets/scss/app.scss ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ }),

/***/ 0:
/*!***********************************************************!*\
  !*** multi ./assets/js/src/app.js ./assets/scss/app.scss ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! C:\xampp\htdocs\medcongress-newmaqueta\assets\js\src\app.js */"./assets/js/src/app.js");
module.exports = __webpack_require__(/*! C:\xampp\htdocs\medcongress-newmaqueta\assets\scss\app.scss */"./assets/scss/app.scss");


/***/ })

/******/ });