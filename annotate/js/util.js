// Utility functions
(function() {
  window.UTIL = {};

  UTIL.lerp = function(a, b, percent) {
    return (1.0*b - a) * percent + a;
  };

  UTIL.lim = function(num, min, max) {
    if (num < min) return min;
    if (num > max) return max;
    return num;
  };

  UTIL.norm = function(value, a, b){
    return (1.0 * value - a) / (b - a);
  };

  UTIL.mean = function(arr){
    var len = arr.length;
    var sum = 0;
    for(var i=0; i<len; i++) {
      sum += arr[i];
    }
    return sum / len;
  };

  UTIL.round = function(value, precision) {
    return value.toFixed(precision);
  };

})();
