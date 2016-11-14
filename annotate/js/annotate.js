'use strict';

var Annotate = (function() {
  function Annotate(options) {
    var defaults = {
      localStorageKey: 'annotations'
    };
    this.opt = _.extend({}, defaults, options);
    this.init();
  }

  Annotate.prototype.init = function(){
    var _this = this;

    this.annotations = {};
    this.currentSegment = -1;
    this.segments = [];
    this.storeLocal = (typeof(Storage) !== "undefined");

    this.dataLoaded = $.Deferred();
    this.annotationsLoaded = $.Deferred();
    this.annotationsLocalLoaded = $.Deferred();

    this.loadAnnotationsLocal(this.opt.localStorageKey);
    this.loadData(this.opt.dataURL);
    this.loadAnnotations(this.opt.annotationsURL);

    $.when(this.dataLoaded, this.annotationsLoaded, this.annotationsLocalLoaded).done(function (data, annotations, annotationsLocal) {
      _this.onLoad(data, annotations, annotationsLocal);
    });
  };

  Annotate.prototype.download = function(){};

  Annotate.prototype.go = function(i){

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
  };

  Annotate.prototype.onLoad = function(originalData, serverAnnotations, localAnnotations){
    var audioPath = this.opt.audioPath;
    var annotations = $.extend({}, serverAnnotations, localAnnotations);

    // put words in line groups
    var lineWords = {};
    $.each(originalData.words, function(i, word){
      if (word.line in lineWords) {
        lineWords[word.line].push(word);
      } else {
        lineWords[word.line] = [word];
      }
    });

    // add lines as audio segments
    var segments = [];
    $.each(originalData.lines, function(i, line){
      var segment = {audioFile: audioPath + "lines/" + line.name + ".wav", label: line.text};
      var lineAnnotations = [];
      $.each(lineWords[i], function(j, word){
        $.each(word.syllables, function(k, syllable){
          if (syllable.name in annotations) {
            lineAnnotations.push(annotations[syllable.name]);
          } else {
            var defaultAnnotation = _this._defaultAnnotation(syllable);
            lineAnnotations.push(defaultAnnotation);
            // annotations[syllable.name] = defaultAnnotation;
          }
        })
      });
      segment.annotations = lineAnnotations;
      segments.push(segment);
    });

    // add non-words as audio segments
    $.each(originalData.nonwords, function(i, word){
      var segment = {audioFile: audioPath + "nonwords/" + word.name + ".wav", label: "Non-word " + (i+1)};
      if (word.name in annotations) {
        segment.annotations = [annotations[word.name]];
      } else {
        var defaultAnnotation = _this._defaultAnnotation(word);
        segment.annotations = [defaultAnnotation];
        // annotations[word.name] = defaultAnnotation;
      }
      segments.push(segment);
    });

    this.annotations = annotations;
    this.segments = segments;

    // add segments to index
    var $index = $('#index');
    $.each(segments, function(i, segment){
      $index.append('<option value="'+i+'">'+segment.label+'</option>');
    });

    this.loadListeners();
    this.goNext();
  };

  Annotate.prototype.playAudio = function(){};

  Annotate.prototype.playBoth = function(){};

  Annotate.prototype.playNotes = function(){};

  Annotate.prototype.saveAnnotationsLocal = function(){
    if (this.storeLocal) {
      localStorage.setItem(this.opt.localStorageKey, JSON.stringify(this.annotations));
    }
  };

  Annotate.prototype._defaultAnnotation = function(obj){
    var defaultAnnotation = {note: '', octave: 0, accent: false, text: false};

    if ("frequency" in obj) {
      $.extend(defaultAnnotation, this._frequencyToNote(obj.frequency));
    }

    return defaultAnnotation;
  };

  Annotate.prototype._frequencyToNote = function(frequency){

    return {note: '', octave: 0};
  };

  Annotate.prototype._initKeys = function(obj, keys){
    $.each(keys, function(i,key){
      if (!(key in obj)) {
        obj[key] = [];
      }
    });
    return obj;
  };

  return Annotate;

})();

$(function(){
  var annotate = new Annotate(CONFIG);
});
