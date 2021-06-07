import pandas as pd
import numpy as np
import os
import matplotlib as mpl
mpl.use('WXAgg')
import matplotlib.pyplot as plt
from cycler import cycler

plt.rc('figure', figsize=(6.4, 4.8), dpi=300, autolayout=True)
plt.rc('lines', linewidth=0.5, markersize=3)
plt.rc('axes', linewidth=0.5,
       prop_cycle=cycler(color=[plt.get_cmap('tab20')(i)
                            for i in range(20)]))


res='2880x1920'
fps=24
video_list=['nyc_drive', 'sunset']
pattern_list = ['1x1', '3x2', '6x4', '9x6', '12x8']
qp_list = [16, 19, 22, 25, 28]

def collect_data():
    data=[]
    columns = ['video','pattern','qp','rate','psnr','spsnr_nn','wspsnr','spsnr_i','cpp_psnr']
    for video in ['nyc_drive', 'sunset']:
        for pattern in ['1x1', '3x2', '6x4', '9x6', '12x8']:
            for qp in [16, 19, 22, 25, 28]:

                name=f'{video}_{res}_{fps}_{pattern}_{qp}'
                with open(f'{name}.txt', 'r') as f:
                    found=False
                    for line in f:
                        if 'Average PSNRS' in line:
                            found=True
                        if found and len(line) > 50:
                            rate = os.path.getsize(f'../encoded/{name}.hvc') * 8 / 60
                            line0 = line.strip()
                            line1 = line0.split('|')
                            line2 = [x.strip() for x in line1 if x]
                            line3 = [[float(i) for i in l.split(' ') if i] for l in line2]
                            line4 = [round(np.average(i),3) for i in line3]

                            data.append([video, pattern, qp, rate,
                                         line4[0],line4[1],line4[2],line4[3],line4[4]])

                            # psnr = line4[0]
                            # spsnr_nn = line4[1]
                            # wspsnr = line4[2]
                            # spsnr_i = line4[3]
                            # cpp_psnr = line4[4]
    dataframe = pd.DataFrame(data, columns=columns)
    dataframe.to_csv('resume.csv')


def graphs():
    dataframe = pd.read_csv('resume.csv')
    fig, [ax1, ax2] = plt.subplots(1,2,figsize=(9.6, 6.8), tight_layout=True)

    for pattern in pattern_list:
        value = dataframe[(dataframe['video']=='nyc_drive') & (dataframe['pattern']==pattern)]
        value2 = dataframe[(dataframe['video']=='sunset') & (dataframe['pattern']==pattern)]

        ax1.plot(value['qp'],value['psnr'], label='psnr')
        ax1.plot(value['qp'],value['spsnr_nn'],label='spsnr_nn')
        ax1.plot(value['qp'],value['spsnr_i'],label='spsnr_i')
        ax1.plot(value['qp'],value['wspsnr'],label='wspsnr')
        ax2.plot(value['qp'], value['rate'], label='rate')
        ax1.legend()
        ax1.set_title(f'nyc_drive_{pattern}')
        ax1.set_xlabel('frame')
        ax1.set_ylabel('Spatial')
        fig.show()


if __name__ == "__main__":
    graphs()
