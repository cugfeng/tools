/*
 * =====================================================================================
 *
 *       Filename:  bmp-color-grayscale.c
 *
 *    Description:  Make BMP image grayscale
 *
 *        Version:  1.0
 *        Created:  04/22/2014 04:15:52 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  cugfeng
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/uio.h>
#include <unistd.h>
#include <fcntl.h>

#define DEBUG

#define LOGI(...) do { \
    fprintf(stdout, __VA_ARGS__); \
    fprintf(stdout, "\n"); \
} while (0)

#ifdef DEBUG
#define LOGE(...) do { \
    fprintf(stderr, "[E][%s][%d]: ", __func__, __LINE__); \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr, "\n"); \
} while (0)
#define LOGD(...) do { \
    fprintf(stdout, "[D][%s][%d]: ", __func__, __LINE__); \
    fprintf(stdout, __VA_ARGS__); \
    fprintf(stdout, "\n"); \
} while (0)
#else
#define LOGE(...) do { \
    fprintf(stderr, __VA_ARGS__); \
    fprintf(stderr, "\n"); \
} while (0)
#define LOGD(...)
#endif

/* BMP file header and info header definition is from Wikipedia.
 * Link: http://en.wikipedia.org/wiki/BMP_file_format */
typedef struct __attribute__ ((__packed__)) _file_header {
    char     magic[2];
    /* the size of the BMP file in bytes */
    unsigned file_size;
    /* reserved; actual value depends on the application that creates the image */
    char     reserved1[2];
    /* reserved; actual value depends on the application that creates the image */
    char     reserved2[2];
    /* the offset, i.e. starting address, of the byte where the bitmap image 
     * data (pixel array) can be found. */
    unsigned offset;
} file_header;

typedef struct __attribute__ ((__packed__)) _info_header {
    /* the size of this header (40 bytes) */
    unsigned header_size;
    /* the bitmap width in pixels (signed integer) */
    int      width;
    /* the bitmap height in pixels (signed integer) */
    int      height;
    /* the number of color planes must be 1 */
    unsigned short no_cp;
    /* the number of bits per pixel, which is the color depth of the image. 
     * Typical values are 1, 4, 8, 16, 24 and 32. */
    unsigned short no_bpp;
    /* the compression method being used. See the next table for a list of 
     * possible values */
    unsigned compression_method;
    /* the image size. This is the size of the raw bitmap data; a dummy 0 
     * can be given for BI_RGB bitmaps. */
    unsigned image_size;
    /* the horizontal resolution of the image. (pixel per meter, signed integer) */
    int      resolution_h;
    /* the vertical resolution of the image. (pixel per meter, signed integer) */
    int      resolution_v;
    /* the number of colors in the color palette, or 0 to default to 2**n */
    unsigned no_colors;
    /* the number of important colors used, or 0 when every color is important;
     * generally ignored */
    unsigned no_important_colors;
} info_header;

#define ROW_SIZE(ih)        ((((ih->no_bpp * ih->width) + 31) >> 5) << 2)
#define ROW_PIXEL_BYTES(ih) ((ih->no_bpp * ih->width) >> 3)

//#define COUNT_GRAYSCALE_VALUE

int parse_header(int fd, file_header *fh, info_header *ih)
{
    int ret = 0;

    assert(fd > 0);
    assert(fh != NULL);
    assert(ih != NULL);

    ret = read(fd, fh, sizeof(file_header));
    if (ret != sizeof(file_header)) {
        LOGE("Read file header failed!");
        return -1;
    }

    ret = read(fd, ih, sizeof(info_header));
    if (ret != sizeof(info_header)) {
        LOGE("Read info header failed!");
        return -2;
    }

    if (ih->image_size == 0) {
        ih->image_size = ROW_PIXEL_BYTES(ih) * ih->height;
    }

    return 0;
}

void dump_header(const file_header *fh, const info_header *ih)
{
    assert(fh != NULL);
    assert(ih != NULL);

    LOGI("width           : %d", ih->width);
    LOGI("height          : %d", ih->height);
    LOGI("bits per pixel  : %d", ih->no_bpp);
    LOGI("pixel array size: %d", ih->image_size);
    LOGI("file size       : %d", fh->file_size);
}

int read_pixel_array(int fd, unsigned char *array, const info_header *ih)
{
    int i, ret, count;
    int row_size = 0;
    int row_pixel_bytes = 0;
    int left_bytes = 0;
    unsigned char *buffer = NULL;

    assert(fd > 0);
    assert(array != NULL);
    assert(ih != NULL);

    row_size = ROW_SIZE(ih);
    row_pixel_bytes = ROW_PIXEL_BYTES(ih);
    left_bytes = ih->image_size;

    buffer = (unsigned char *)malloc(row_size);
    assert(buffer != NULL);
    for (i = 0; i < ih->height; ++i) {
        assert(left_bytes > 0);

        count = (row_pixel_bytes > left_bytes) ? left_bytes : row_pixel_bytes;

        memset(buffer, 0, row_size);
        ret = read(fd, buffer, row_size);
        if (ret != row_size) {
            LOGE("Read pixel array failed!");
            ret = -1;
            break;
        }
        memcpy(array, buffer, count);

        array += count;
        left_bytes -= count;
    }
    free(buffer);
    buffer = NULL;

    return ret;
}

/* RGB to/from YUV conversion is from Wikipedia.
 * Link: http://en.wikipedia.org/wiki/YUV
 * Only keep Y channel for YUV, U and V channels are default as zero */
void color_to_grayscale(unsigned char *array, int size)
{
    int i;
    float y;
    unsigned char r, g, b;

    for (i = 0; i < size; i += 3) {
        r = array[i + 0];
        g = array[i + 1];
        b = array[i + 2];
        y = (float)(0.299 * r + 0.587 * g + 0.114 * b);
        array[i + 0] = (unsigned char)y;
        array[i + 1] = (unsigned char)y;
        array[i + 2] = (unsigned char)y;
    }
}

int write_header(int fd, const file_header *fh, const info_header *ih)
{
    int ret = 0;

    assert(fd > 0);
    assert(fh != NULL);
    assert(ih != NULL);

    ret = write(fd, fh, sizeof(file_header));
    if (ret != sizeof(file_header)) {
        LOGE("Write file header failed!");
        return -1;
    }

    ret = write(fd, ih, sizeof(info_header));
    if (ret != sizeof(info_header)) {
        LOGE("Write info header failed!");
        return -1;
    }

    return 0;
}

int write_pixel_array(int fd, const unsigned char *array, const info_header *ih)
{
    int i, ret, count;
    int row_size = 0;
    int row_pixel_bytes = 0;
    int left_bytes = 0;
    unsigned char *buffer = NULL;

    assert(fd > 0);
    assert(array != NULL);
    assert(ih != NULL);

    row_size = ROW_SIZE(ih);
    row_pixel_bytes = ROW_PIXEL_BYTES(ih);
    left_bytes = ih->image_size;

    buffer = (unsigned char *)malloc(row_size);
    assert(buffer != NULL);
    for (i = 0; i < ih->height; ++i) {
        assert(left_bytes > 0);

        count = (row_pixel_bytes > left_bytes) ? left_bytes : row_pixel_bytes;

        memset(buffer, 0, row_size);
        memcpy(buffer, array, count);
        ret = write(fd, buffer, row_size);
        if (ret != row_size) {
            LOGE("Write pixel array failed!");
            ret = -1;
            break;
        }

        array += count;
        left_bytes -= count;
    }
    free(buffer);
    buffer = NULL;

    return ret;
}

#ifdef COUNT_GRAYSCALE_VALUE
void count_grayscale_value(const unsigned char *array, int size)
{
    int i = 0;
    int count[256] = {0};

    assert(array != NULL);

    for (i = 0; i < size; i += 3) {
        ++count[array[i]];
    }

    for (i = 0; i < 256; ++i) {
        LOGI("%d", count[i]);
    }
}
#endif

void process_bmp_file(int fd_in, int fd_out)
{
    file_header fh;
    info_header ih;
    unsigned char *pixel_array = NULL;

    memset(&fh, 0, sizeof(file_header));
    memset(&ih, 0, sizeof(info_header));

    LOGD("Parse BMP header");
    parse_header(fd_in, &fh, &ih);
    dump_header(&fh, &ih);

    pixel_array = (unsigned char *)malloc(ih.image_size);
    assert(pixel_array != NULL);

    LOGD("Read BMP pixel array");
    read_pixel_array(fd_in, pixel_array, &ih);
    LOGD("Convert color to grayscale");
    color_to_grayscale(pixel_array, ih.image_size);

    LOGD("Write BMP header");
    write_header(fd_out, &fh, &ih);
    LOGD("Write BMP pixel array");
    write_pixel_array(fd_out, pixel_array, &ih);
    LOGD("Done");

#ifdef COUNT_GRAYSCALE_VALUE
    LOGD("Count grayscale value");
    count_grayscale_value(pixel_array, ih.image_size);
    LOGD("Done");
#endif

    free(pixel_array);
    pixel_array = NULL;
}

void usage(char *prog)
{
    LOGI("%s input.bmp output.bmp", prog);
}

int main(int argc, char *argv[])
{
    int ret    = 0;
    int fd_in  = 0;
    int fd_out = 0;

    if (argc != 3) {
        usage(argv[0]);
        return 0;
    }

    fd_in = open(argv[1], O_RDONLY);
    if (fd_in < 0) {
        LOGE("Open file %s failed!", argv[1]);
        ret = -1;
        goto exit_1;
    }

    unlink(argv[2]);
    fd_out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC);
    if (fd_out < 0) {
        LOGE("Open file %s failed!", argv[2]);
        ret = -1;
        goto exit_2;
    }

    process_bmp_file(fd_in, fd_out);

    close(fd_out);
    chmod(argv[2], S_IRUSR | S_IXUSR);
exit_2:
    close(fd_in);
exit_1:
    return ret;
}

