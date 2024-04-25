from csv2gif import CSV2GIF


def temp_data():
    in_fp = "US_City_Temp_Data.csv"
    out_fp = "output"
    gif = CSV2GIF(in_fp)

    x_series = ["boston", "chicago", "san_francisco"]
    gif.ax.set_ylabel("counts")
    gif.ax.set_xlabel("temperature")

    gif.build_Z_gif(out_fp, x_series, z_label="month", style="violinplot",
                    total_length=10, hold=0, color="red", bins=20)
    return 0


def olympic_data():
    in_fp = "athlete_events.csv"
    out_fp = "athlete_out"
    gif = CSV2GIF(in_fp)
    gif.build_xy_gif(out_fp, x_label="Height", y_label="Weight", z_label="Games",
                     total_length=10, hold=0, style="scatter", color="red")


if __name__ == '__main__':
    temp_data()
    olympic_data()
