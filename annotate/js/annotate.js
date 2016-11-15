'use strict';

var Annotate = (function() {
  function Annotate(options) {
    var defaults = {
      localStorageKey: 'annotations',
      minOctave: 1,
      maxOctave: 4
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

    $.when(this.dataLoaded, this.annotationsLoaded, this.annotationsLocalLoaded).done(function (data, annotations, annotationsLocal) {
      _this.onLoad(data, annotations, annotationsLocal);
    });
  };

  Annotate.prototype.download = function(){};

  Annotate.prototype.getAccentSelect = function(selectedAccent){
    var accents = ['', 'ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff'];
    var $select = $('<select class="select-accent">');
    $.each(accents, function(i, accent){
      var selected = accent==selectedAccent ? ' selected' : '';
      $select.append('<option value="'+accent+'"'+selected+'>'+accent+'</option>');
    });
    return $select;
  };

  Annotate.prototype.getNoteSelect = function(selectedNote){
    var notes = this._notes();
    var minOctave = this.opt.minOctave;
    var maxOctave = this.opt.maxOctave;
    var $select = $('<select class="select-note-octave">');
    for (var octave=minOctave; octave <= maxOctave; octave++) {
      $.each(notes, function(i, note){
        var noteOctave = note+octave;
        var selected = noteOctave==selectedNote ? ' selected' : '';
        $select.append('<option value="'+noteOctave+'"'+selected+'>'+noteOctave+'</option>');
      });
    }
    return $select;
  };

  Annotate.prototype.go = function(i){
    var _this = this;
    var segment = this.segments[i];

    // load text
    // $('#text').text(segment.label);
    $('#index').val(i);

    // load annotations
    var $annotations = $('<div>');
    var aWidth = (1.0 / segment.annotations.length) * 100;
    $.each(segment.annotations, function(i, a){
      var $a = $('<div class="annotation">');
      $a.append($('<label>'+a.text+'</label>'));
      $a.append(_this.getNoteSelect(a.note+a.octave));
      $a.append(_this.getAccentSelect(a.accent));
      $a.css('width', aWidth + '%');
      $annotations.append($a);
    });
    $('#annotations').html($annotations);
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
          // TODO: add start
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

    this.loadSegments(segments);
    this.loadListeners();
    this.goNext();
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

  Annotate.prototype.saveAnnotationsLocal = function(){
    if (this.storeLocal) {
      localStorage.setItem(this.opt.localStorageKey, JSON.stringify(this.annotations));
    }
  };

  Annotate.prototype._defaultAnnotation = function(obj){
    var defaultAnnotation = {note: 'C', octave: 0, accent: '', text: ''};

    if ("frequency" in obj) {
      $.extend(defaultAnnotation, this._frequencyToNote(obj.frequency));
    }

    if ("text" in obj){
      defaultAnnotation.text = obj.text;
    }

    return defaultAnnotation;
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

  Annotate.prototype._initKeys = function(obj, keys){
    $.each(keys, function(i,key){
      if (!(key in obj)) {
        obj[key] = [];
      }
    });
    return obj;
  };

  Annotate.prototype._notes = function(){
    return ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  };

  return Annotate;

})();

$(function(){
  var annotate = new Annotate(CONFIG);
});
