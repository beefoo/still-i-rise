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
    this.opt = $.extend({}, defaults, options);
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

    $('.play-audio').on('click', function(e){ _this.playAudio(); });
    $('.play-notes').on('click', function(e){ _this.playNotes(); });
    $('.play-both').on('click', function(e){ _this.playBoth(); });

    $('.download').on('click', function(e){ _this.download(); });

    $(window).on('resize', function(e){ _this.onResize(); });
  };

  Annotate.prototype.loadSegments = function(segments){
    // add segments to index
    var $index = $('#index');
    $.each(segments, function(i, segment){
      $index.append('<option value="'+i+'">'+segment.label+'</option>');
    });
  };

  Annotate.prototype.onLoad = function(originalData, serverAnnotations, localAnnotations){
    var _this = this;
    var audioPath = this.opt.audioPath;
    var annotations = $.extend({}, serverAnnotations, localAnnotations);

    this.frequencyRange = [Math.floor(originalData.minFrequency), Math.ceil(originalData.maxFrequency)];
    this.intensityRange = [Math.floor(originalData.minIntensity), Math.ceil(originalData.maxIntensity)];

    // put item in groups
    var groupItems = {};
    $.each(originalData.data, function(i, item){
      if (item.group in groupItems) {
        groupItems[item.group].push(item);
      } else {
        groupItems[item.group] = [item];
      }
    });

    // add lines as audio segments
    var segments = [];
    $.each(originalData.groups, function(i, group){
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

    $.each(items, function(i, item){
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
      ctx.textAlign = "center";
      ctx.font = opt.font;
      ctx.fillStyle = opt.textStyle;
      ctx.fillText(item.text, x + (x1-x)*0.5, 30);

      // draw frames
      $.each(item.frames, function(j, frame){
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
    });
  };

  Annotate.prototype.saveAnnotationsLocal = function(){
    if (this.storeLocal) {
      localStorage.setItem(this.opt.localStorageKey, JSON.stringify(this.annotations));
    }
  };

  Annotate.prototype._frequencyToNote = function(frequency){
    var note = {note: 'C', octave: 0};
    var notes = this._notes();
    if (frequency > 0) {
      var A4 = 440;
      var C0 = A4 * Math.pow(2, -4.75);
      var h = Math.round(12*(Math.log(frequency/C0)/Math.log(2)));
      note.octave = Math.floor(h / 12);
      note.note = notes[h % 12];
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
