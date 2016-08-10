# vehicle-ymm

Vehicle years, makes, and models.

### install

    npm i --save vehicle-ymm

### use

```javascript
var vymm = require('vehicle-ymm');
var ymm = [
  vymm[0].models[0].years[0],
  vymm[0].make,
  vymm[0].models[0].model
].join(' ');
console.log(ymm);
// '2003 Acura CL'
```
