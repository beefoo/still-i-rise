'use strict';

var Annotate = (function() {
  function Annotate(options) {
    var defaults = {
      alphaRange: [0.1, 1],
      bgStyle: '#111111',
      dotRadius: 2,
      font: '18px sans-serif',
      localStorageKey: 'annotations',
      strokeStyle: '#555555',
      textStyle: '#ffffff'
    };
    this.opt = _.extend({}, defaults, options);
    this.init();
  }

  Annotate.prototype.init = function(){
    var _this = this;

    this.annotations = {};
    this.sounds = {};
    this.currentSegment = -1;
    this.segments = [];
    this.storeLocal = (typeof(Storage) !== "undefined");

    this.dataLoaded = $.Deferred();
    this.annotationsLoaded = $.Deferred();
    this.annotationsLocalLoaded = $.Deferred();

    this.loadAnnotationsLocal(this.opt.localStorageKey);
    this.loadData(this.opt.dataURL);
    this.loadAnnotations(this.opt.annotationsURL);
    this.loadCanvas();

    $.when(this.dataLoaded, this.annotationsLoaded, this.annotationsLocalLoaded).done(function (data, annotations, annotationsLocal) {
      _this.onLoad(data, annotations, annotationsLocal);
    });
  };

  Annotate.prototype.download = function(){};

  Annotate.prototype.go = function(i){
    var _this = this;
    var segment = this.segments[i];
    this.currentSegment = i;

    // load text
    // $('#text').text(segment.label);
    $('#index').val(i);

    this.renderCanvas();
  };

  Annotate.prototype.goNext = function(){
    this.currentSegment += 1;
    if (this.currentSegment >= this.segments.length) this.currentSegment = this.segments.length - 1;
    this.go(this.currentSegment);
  };

  Annotate.prototype.goPrevious = function(){
    this.currentSegment -= 1;
    if (this.currentSegment < 0) this.currentSegment = 0;
    this.go(this.currentSegment);
  };

  Annotate.prototype.guessPitch = function(frames){
    // no frames
    if (!frames.length) return [];

    // break frames into groups
    var groups = [];
    var group = [];
    var threshold = 10; // don't jump more than x Hz
    var lastF = 0;
    _.each(frames, function(f, i){
      var delta = Math.abs(f[1] - lastF);

      // frame is continuation of last frame
      if (f[1] > 0 && (delta <= threshold || lastF <= 0)) {
        group.push(f);

      // frame jumped high, add existing group, start a new group
      } else if (f[1] > 0) {
        if (group.length) groups.push(group);
        group = [f];

      // frame is silent, add existing group
      } else {
        if (group.length) groups.push(group);
        group = [];
      }

      lastF = f[1];
    });
    if (group.length) groups.push(group);

    // map groups
    groups = _.map(groups, function(g){
      return {
        start: g[0][0],
        intensity: (_.reduce(g, function(memo, f){ return memo + f[2]; }, 0) / g.length),
        size: g.length,
        frames: g
      }
    });

    // sort groups
    groups.sort(function(a, b){
      var aScore = a.size * a.intensity;
      var bScore = b.size * b.intensity;
      // first sort by score, desc
      if (aScore < bScore) return 1;
      else if (aScore > bScore) return -1;
      // then by intensity, desc
      else if (a.intensity < b.intensity) return 1;
      else if (a.intensity > b.intensity) return -1;
      // then by start, desc
      else if (a.start < b.start) return 1;
      else if (a.start > b.start) return -1;
      else return 0;
    });

    // choose the first group
    if (!groups.length) return [];
    frames = groups[0].frames;

    // sort by intensity
    frames = _.sortBy(frames, function(f){ return -f[2] });

    // only take the most intense
    frames = frames.slice(0, Math.ceil(frames.length * 0.5));

    // get frames before and after peak
    var maxFrame = _.max(frames, function(f){ return f[1]; });
    var framesLeft = _.filter(frames, function(f){ return f[0] < maxFrame[0]});
    var framesRight = _.filter(frames, function(f){ return f[0] > maxFrame[0]});

    // take the high and low
    var minFrameLeft = framesLeft.length ? _.min(framesLeft, function(f){ return f[1]; }) : false;
    var minFrameRight = framesRight.length ? _.min(framesRight, function(f){ return f[1]; }) : false;
    frames = [maxFrame];
    if (minFrameLeft) frames.push(minFrameLeft);
    if (minFrameRight) frames.push(minFrameRight);

    // sort by time
    frames = _.sortBy(frames, function(f){ return f[0] });

    return frames;
  }

  Annotate.prototype.loadAnnotations = function(url){
    var _this = this;
    $.getJSON(url, function(data) {
      console.log("Annotation file loaded.");
      _this.annotationsLoaded.resolve(data);
    })
    .fail(function() {
      console.log("No annotation file found. Initializing with empty annotations");
      _this.annotationsLoaded.resolve({});
    });
  };

  Annotate.prototype.loadAnnotationsLocal = function(key){
    var annotationsLocal = {};
    if (this.storeLocal) {
      if (localStorage[key]) {
        console.log("Local annotations loaded.");
        annotationsLocal = JSON.parse(localStorage[key]);
      } else {
        console.log("No local annotations found. Initializing to empty annotations");
      }
    } else {
      alert('Browser does not support localStorage. Annotations will be lost upon browser refresh.')
    }
    this.annotationsLocalLoaded.resolve(annotationsLocal);
  };

  Annotate.prototype.loadCanvas = function(){
    this.$canvasContainer = $('#canvas-container');
    this.$canvas = $('#canvas');
    this.canvas = this.$canvas[0];
    this.ctx = this.canvas.getContext("2d");
    this.canvas.width  = this.$canvasContainer.width();
    this.canvas.height = this.$canvasContainer.height();
  };

  Annotate.prototype.loadData = function(url){
    var _this = this;
    $.getJSON(url, function(data) {
      console.log("Data file loaded.");
      _this.dataLoaded.resolve(data);
    });
  };

  Annotate.prototype.loadListeners = function(){
    var _this = this;

    $('.previous').on('click', function(e){ _this.goPrevious(); });
    $('.next').on('click', function(e){ _this.goNext(); });
    $('.index').on('change', function(e){
      var val = parseInt($(this).val());
      if (val >= 0) _this.go(val);
    });
    $(window).on('keydown', function(e){
      if (e.keyCode == 37) { e.preventDefault(); _this.goPrevious(); }
      else if (e.keyCode == 39) { e.preventDefault(); _this.goNext(); }
      else if (e.keyCode == 32) { e.preventDefault(); _this.playAudio(); }
    })

    $('.play-audio').on('click', function(e){ _this.playAudio(); });
    $('.play-notes').on('click', function(e){ _this.playNotes(); });
    $('.play-both').on('click', function(e){ _this.playBoth(); });

    $('.download').on('click', function(e){ _this.download(); });

    $(window).on('resize', function(e){ _this.onResize(); });
  };

  Annotate.prototype.loadSegments = function(segments){
    // add segments to index
    var $index = $('#index');
    _.each(segments, function(segment, i){
      $index.append('<option value="'+i+'">'+segment.label+'</option>');
    });
  };

  Annotate.prototype.onLoad = function(originalData, serverAnnotations, localAnnotations){
    var _this = this;
    var audioPath = this.opt.audioPath;
    var annotations = _.extend({}, serverAnnotations, localAnnotations);

    this.frequencyRange = [Math.floor(originalData.minFrequency), Math.ceil(originalData.maxFrequency)];
    this.intensityRange = [Math.floor(originalData.minIntensity), Math.ceil(originalData.maxIntensity)];

    // put item in groups
    var groupItems = {};
    _.each(originalData.data, function(item, i){
      if (item.group in groupItems) {
        groupItems[item.group].push(item);
      } else {
        groupItems[item.group] = [item];
      }
    });

    // add lines as audio segments
    var segments = [];
    _.each(originalData.groups, function(group, i){
      var segment = {name: group.name, audioFile: audioPath + group.type + "/" + group.name + ".wav", label: group.text};
      segment.items = groupItems[group.name];
      segments.push(segment);
    });

    this.annotations = annotations;
    this.segments = segments;

    this.loadSegments(segments);
    this.loadListeners();
    this.goNext();
  };

  Annotate.prototype.onResize = function(){
    this.canvas.width  = this.$canvasContainer.width();
    this.canvas.height = this.$canvasContainer.height();
    this.renderCanvas();
  };

  Annotate.prototype.playAudio = function(){
    var segment = this.segments[this.currentSegment];
    console.log('Playing '+segment.audioFile);

    if (!(this.currentSegment in this.sounds)) {
      this.sounds[this.currentSegment] = new Howl({
        src: [segment.audioFile]
      });
    }

    this.sounds[this.currentSegment].play();
  };

  Annotate.prototype.playBoth = function(){
    this.playAudio();
    this.playNotes();
  };

  Annotate.prototype.playNotes = function(){
    var segment = this.segments[this.currentSegment];
  };

  Annotate.prototype.renderCanvas = function(){
    var _this = this;
    var segment = this.segments[this.currentSegment];
    var items = segment.items;
    var start = items[0].start;
    var end = items[items.length-1].end;
    var fRange = this.frequencyRange;
    var ctx = this.ctx;
    var w = this.canvas.width;
    var h = this.canvas.height;
    var opt = this.opt;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = opt.bgStyle;
    ctx.rect(0, 0, w, h);
    ctx.fill();

    _.each(items, function(item, i){
      var x = UTIL.norm(item.start, start, end) * w;
      // draw line
      if (i > 0) {
        ctx.strokeStyle = opt.strokeStyle;
        ctx.beginPath();
        ctx.moveTo(x,0);
        ctx.lineTo(x,h);
        ctx.stroke();
      }

      // draw text
      var x1 = UTIL.norm(item.end, start, end) * w;
      var centerX = x + (x1-x)*0.5;
      ctx.textAlign = "center";
      ctx.font = opt.font;
      ctx.fillStyle = opt.textStyle;
      ctx.fillText(item.text, centerX, 30);

      // draw frames
      var frames = item.frames;
      _.each(frames, function(frame, j){
        var fStart = frame[0];
        var frequency = frame[1];
        var intensity = frame[2];
        var fx = UTIL.norm(fStart, start, end) * w;
        var fy = UTIL.norm(frequency, fRange[1], fRange[0]) * h;

        ctx.beginPath();
        ctx.fillStyle = "rgba(255,255,255,"+UTIL.lerp(opt.alphaRange[0], opt.alphaRange[1], intensity)+")";
        ctx.arc(fx,fy,opt.dotRadius,0,2*Math.PI);
        ctx.fill();
      });

      // draw guess
      var pitch = _this.guessPitch(frames);
      if (pitch.length === 1) {
        var px = UTIL.norm(pitch[0][0], start, end) * w;
        var py = UTIL.norm(pitch[0][1], fRange[1], fRange[0]) * h;
        py = UTIL.lim(py, 1, h-1);
        ctx.beginPath();
        ctx.fillStyle = "red";
        ctx.arc(px,py,opt.dotRadius,0,2*Math.PI);
        ctx.fill();

      } else if (pitch.length >= 2) {
        ctx.strokeStyle = 'red';
        ctx.beginPath();
        _.each(pitch, function(p, j){
          var px = UTIL.norm(p[0], start, end) * w;
          var py = UTIL.norm(p[1], fRange[1], fRange[0]) * h;
          py = UTIL.lim(py, 1, h-1);
          if (j===0) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        });
        ctx.stroke();
      }
    });
  };

  Annotate.prototype.saveAnnotationsLocal = function(){
    if (this.storeLocal) {
      localStorage.setItem(this.opt.localStorageKey, JSON.stringify(this.annotations));
    }
  };

  Annotate.prototype._frequencyToNote = function(frequency){
    var note = false;
    if (frequency > 0) {
      var A4 = 440;
      var C0 = A4 * Math.pow(2, -4.75);
      var h = Math.round(12*(Math.log(frequency/C0)/Math.log(2)));
      note.octave = Math.floor(h / 12);
      note.note = Math.floor(h % 12);
    }
    return note;
  };

  Annotate.prototype._notes = function(){
    return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  };

  return Annotate;

})();

$(function(){
  var annotate = new Annotate(CONFIG);
});
