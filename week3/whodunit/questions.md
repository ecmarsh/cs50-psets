# Questions

## What's `stdint.h`?

`stdint.h` is a C lib header file

- Intended to allow programmers to write more portable code
- Provides a set of typedefs that specify:
- - Exact-width integer types, together with the defined minimum and maximum allowable values for each type, using macros .

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

- To define the sizes of variables across different machines.
- The `_t` is added to standardize it across platforms too.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

_recall: 1 byte = 8 bits_
Alias | Size (bytes)
----- | -------
BYTE | 1 byte
DWORD | 4 bytes
LONG | 4 bytes
WORD | 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

**Byte 1: "B"**
**Byte 2: "M"**

- The first 2 bytes of the BMP file format are the character "B" then the character "M" in ASCII encoding.
- All of the integer values are stored in little-endian format (i.e. least-significant byte first).

## What's the difference between `bfSize` and `biSize`?

- `biSize` : The number of bytes required by the structure.
- `bfSize` : The size, in bytes, of the bitmap file.

## What does it mean if `biHeight` is negative?

- That thee bitmap is a top-down device-independent bitmap (DIB) with the origin at the upper left corner.
- - _Note_: biHeight must be positive, regardless of image orientation.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount`

- Specifies the number of bits per pixel (bpp).
- - For uncompressed formats, this value is the avg number of bpp.
- - For compressed formats, this value is the implied bit depth of the uncompressed image, _after_ the image has been decoded.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

- If the file doesn't exist, or no/wrong infile was provided.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

- This refers to the number of elements. We are only reading (BITMAPINFOHEADER), so we use 1.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

```C
// determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // bi.biWidth = 3
    padding = (4 - (3 * 3) % 4) % 4;
            = (4 - (9) % 4) % 4;
            = (4 - 1) % 4;
            = 3 % 4
            = 3
```

\*\*Line 63 assigns `padding` to `3` if `bi.biwidth` is `3`

## What does `fseek` do?

> Allows you to rewind or fast-foward withina . file

- Analagy was a dvd player and setting how far along you are in movie.
- Definition: sets the file position of `stream` (first argument) to the given `offset` (2nd argument)

##### USAGE

```C
int fseek(FILE *stream, long int offset, int whence)
    // stream - ptr to a FILE object that identifies the stream
    // offset - number of bytes to offset from whence
    // whence - position from where offset is added. Specified as one of
        // SEEK_SET (beginning of file)
        // SEEK_CUR (cur position of file ptr)
        // SEEK_SET (end of file (EOF)
```

## What is `SEEK_CUR`?

`SEEK_CUR` is a constant int that specifies where to offset from

- Current position of the file pointer
