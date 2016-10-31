0 => int padding_start;
2000 => int padding_end;
3 => int instrument_buffers;
0 => int start;
me.sourceDir() => string base_dir;

// normalize base directory
if (base_dir.charAt(base_dir.length()-1) != '/')
{
    "/" +=> base_dir;
}

// read sequence file
base_dir + "data/ck_sequence.csv" => string sequence_file;
FileIO sequence_fio;
sequence_fio.open( sequence_file, FileIO.READ );

// check if file is valid
if( !sequence_fio.good() )
{
    cherr <= "can't open sequence file for reading..."
          <= IO.newline();
    me.exit();
}

// Add padding
padding_start::ms => now;
padding_start => int elapsed_ms;

// read sequence from file
while( sequence_fio.more() ) {
    sequence_fio.readLine() => string filename;
    Std.atof(sequence_fio.readLine()) => float gain;
    Std.atoi(sequence_fio.readLine()) => int milliseconds;

    // remove carriage return if found
    filename.find("\r") => int return_match;
    if (return_match >= 0)
    {
        filename.erase(return_match, 1);
    }

    // open file as sound buffer
    base_dir + filename => filename;
    SndBuf buf;
    filename => buf.read;
    buf.samples() => buf.pos; // don't play immediately after opening
    buf => dac;

    elapsed_ms + milliseconds => elapsed_ms;
    if (start > elapsed_ms)
    {
        continue;
    }

    // wait duration
    if (milliseconds > 0)
    {
        milliseconds::ms => now;
    }

    // play the instrument
    0 => buf.pos;
    gain => buf.gain;
}

// Add padding
padding_end::ms => now;

<<< "Done." >>>;
