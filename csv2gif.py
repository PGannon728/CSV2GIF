import imageio.v2 as imageio
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil
import re
import argparse


class CSV2GIF:
    def __init__(self, data_file_path, ) -> None:
        """
           Initializes class and imports CSV data

           Parameters:
           data_file_path (string): Relative filepath of document

           Returns:
           None
           """
        self.data_fp = data_file_path
        # read in data
        self.df = pd.read_csv(self.data_fp)

        # setup plot
        self.fig, self.ax = plt.subplots()
        pass

    def _build_xy_plot(self, x_label, y_label, z_label, z_val,
                       style, color="blue",
                       linestyle="-", marker=".",
                       ):
        """
            Private class to generate plot a single frame of gif

            Parameters:
            x_label (string): X label of CSV data
            y_label (string): Y label of CSV data
            z_val (string): Z value to be plotted
            style (string): style of plot in use
            color (string): color selection of plot points
            linestyle (string): line style of plot (line plot only)
            marker (string): Marker style of plot (scatter and line plot only)


            Returns:
            points (tuple): matplotlib object containing plot objects
            """
        z_df = self._create_z_slice(z_label, z_val)
        x_axis = z_df[x_label].values.tolist()
        y_axis = z_df[y_label].values.tolist()

        self.ax.set_title((z_label + ":\t" + str(z_val)).expandtabs())
        # self.ax.set_xlabel(x_label)
        # self.ax.set_ylabel(y_label)
        if style == "scatter":
            points = self.ax.scatter(x_axis, y_axis, color=color, marker=marker)

        elif style == "line":
            points = self.ax.plot(x_axis, y_axis, color=color, marker=marker, linestyle=linestyle)

        elif style == "bar":
            points = self.ax.bar(x_axis, y_axis, color=color)

        else:
            print("invalid style")
            return None
        return points

    def build_xy_gif(self, output_filepath, x_label, y_label, z_label,
                     total_length=10, style="scatter", color="blue",
                     linestyle="-", marker="o", hold=0,
                     ):
        """
            Public class to generate plot a gif

            Parameters:
            output_filepath (string): X label of CSV data
            x_label (string): X label of CSV data
            y_label (string): Y label of CSV data
            z_label (string): Z label of CSV data
            total_length (int): length (sec) of GIF
            style (string): style of plot in use
            color (string): color selection of plot points
            linestyle (string): line style of plot (line plot only)
            marker (string): Marker style of plot (scatter and line plot only)
            hold (bool): if true, do not erase old plots

            Returns:
            None
            """
        images = []
        if os.path.isdir(output_filepath):
            shutil.rmtree(output_filepath)
            os.mkdir(output_filepath)
        else:
            os.mkdir(output_filepath)

        files = []
        x_min = min(self.df[x_label])
        x_max = max(self.df[x_label])
        y_min = min(self.df[y_label])
        y_max = max(self.df[y_label])

        for value in self.df[z_label].unique():
            self._build_xy_plot(x_label, y_label, z_label, z_val=value, style=style, color=color, linestyle=linestyle, marker=marker)
            self.ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max))
            save_fn = output_filepath + "/" + str(value)
            files.append(save_fn + ".png")
            plt.savefig(save_fn)

            if not hold:
                for col in list(self.ax.collections):
                    col.remove()
                for art in list(self.ax.lines):
                    art.remove()
                for cont in list(self.ax.containers):
                    cont.remove()

        self.imgs2gif(output_filepath, output_filepath, total_length=total_length)
        pass

    def build_Z_gif(self, output_filepath, x_series, z_label, style,
                    total_length=10, hold=0, color="red", bins=10, medians=True
                    ):
        """
            Public class to generate plot a gif

            Parameters:
            output_filepath (string): X label of CSV data
            x_series (string): X label of CSV data
            z_label (string): Z value to be plotted
            style (string): style of plot in use
            total_length (string): length of GIF (sec)
            hold (bool): if tture, do not erase old plots
            color (string): color selection of plot fills
            bins (int): number of bins for histogram
            medians(bool): display median bars on violin/boxplot

            Returns:
            None
            """

        images = []
        if os.path.isdir(output_filepath):
            shutil.rmtree(output_filepath)
            os.mkdir(output_filepath)
        else:
            os.mkdir(output_filepath)

        files = []

        y_min = self.df[x_series].min().min()
        y_max = self.df[x_series].max().max()

        for value in self.df[z_label].unique():
            self._build_Z_plot(x_series, z_label, z_val=value, style=style, y_min=y_min, y_max=y_max,
                               color=color, bins=bins, medians=medians)
            save_fn = output_filepath + "/" + str(value)
            files.append(save_fn + ".png")
            plt.savefig(save_fn)

            if not hold:
                for art in list(self.ax.lines):
                    art.remove()
                for cont in list(self.ax.containers):
                    cont.remove()
                for coll in list(self.ax.collections):
                    coll.remove()
                for box in list(self.ax.patches):
                    box.remove()

        self.imgs2gif(str(output_filepath), str(output_filepath), total_length=total_length)
        pass

    def _build_Z_plot(self, x_series, z_label, z_val, style, y_min, y_max,
                      color, bins, medians,):

        """
            Private class to generate plot a single frame of gif

            Parameters:
            output_filepath (string): X label of CSV data
            x_series (string): X label of CSV data
            z_label (string): Z label to be plotted
            z_val (string): Z value to be plotted
            style (string): style of plot in use
            y_min (float): minimum y-axis value
            y_max (float): maximum y-axis value
            color (string): color selection of plot fills
            bins (int): number of bins for histogram
            medians(bool): display median bars on violin/boxplot

            Returns:
            points (tuple): matplotlib object containing plot
            """
        z_df = self._create_z_slice(z_label, z_val)
        data = z_df[x_series].values

        self.ax.set_title((z_label + ":\t" + str(z_val)).expandtabs())
        if style == "boxplot":
            self.ax.set(ylim=(y_min, y_max))
            points = self.ax.boxplot(data, patch_artist=True)
            for box in points['boxes']:
                box.set_facecolor(color)

        elif style == "violinplot":
            self.ax.set(ylim=(y_min, y_max))
            points = self.ax.violinplot(data, showmedians=medians)
            for box in points['bodies']:
                box.set_color(color)
                box.set_edgecolor(color)
            points['cmedians'].set_colors(color)
            points['cbars'].set_colors(color)
            points['cmins'].set_colors(color)
            points['cmaxes'].set_colors(color)

        elif style == "hist":
            self.ax.set(xlim=(y_min, y_max))
            points = self.ax.hist(data, color=color, bins=bins)
        else:
            print("invalid")
            return None
        return points

    def _create_z_slice(self, z_label, z_val):
        """
            Extract values of z_label with value z_val

            Parameters:
            z_label (string): Z label to be plotted
            z_val (string): Z value to be plotted

            Returns:
            df [df]: Dataframe where z_label == z_val
            """
        return self.df[(self.df[z_label] == z_val).values.tolist()]

    @staticmethod
    def imgs2gif(in_foldername, out_filename, total_length=10):
        """
            Create GIF from series of images

            Parameters:
            in_foldername (string): input folder location
            out_filename (string): desired output name

            Returns:
            None
            """

        # Get a list of all file names in the directory
        file_names = os.listdir(in_foldername)

        def alphanumeric_sort(_file_names):
            def convert(text):
                return int(text) if text.isdigit() else text.lower()

            def alphanum_key(key):
                return [convert(c) for c in re.split('([0-9]+)', key)]

            return sorted(_file_names, key=alphanum_key)

        sorted_file_names = alphanumeric_sort(file_names)

        images = []
        for fn in sorted_file_names:
            images.append(imageio.imread(str(in_foldername + "\\" + fn)))

        frame_duration = total_length / os.listdir(in_foldername).__len__()
        sn = str(out_filename) + ".gif"
        imageio.mimwrite(sn, images, "GIF", duration=frame_duration / .001, loop=0)
        pass


def default_split():
    """
        Create GIF from CSV data. Used for CLI interface. Use -h argument for more details

        Returns:
        None
        """
    parser = argparse.ArgumentParser(description='csv2gif description')
    parser.add_argument('-fp', '--filepath',
                        help='File location/name of *.csv file. Acceptsabsolute and relative paths', required=True)
    parser.add_argument('-x', '--xlabel', help='Column name for X axis', required=True)
    parser.add_argument('-y', '--ylabel', help='Column name for Y axis', required=True)
    parser.add_argument('-z', '--zlabel', help='Column name for Z axis', required=True)
    parser.add_argument('-dr', '--duration', help='Total duration of gif (seconds)', required=False, default=10)
    args = vars(parser.parse_args())
    # print(args)

    in_fp = args['filepath']
    duration = float(args['duration'])
    x_lab = args['xlabel']
    y_lab = args['ylabel']
    z_lab = args['zlabel']

    out_fp = "output"
    gif = CSV2GIF(in_fp)
    gif.build_xy_gif(out_fp, x_label=x_lab, y_label=y_lab, z_label=z_lab, total_length=duration)
    return None


if __name__ == '__main__':
    default_split()
