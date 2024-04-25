from csv2gif import CSV2GIF


if __name__ == '__main__':
    in_fp = "output_untrained/output_full"
    out_fp = "super_trained_gif"
    duration = 15
    CSV2GIF.imgs2gif(in_fp, out_fp, duration)

