import { Injectable } from '@angular/core';
import { Stats } from '../../../services/models';

import * as echarts from 'echarts';

@Injectable({
  providedIn: 'root'
})
export class ColumnChartService {

  createColumnChartWithGradient(stats: Stats[]) {
    var option = {
      title: {
        text: 'Stats Overview : TOP 10'
      },
      xAxis: {
        data: this._namesForColumnChart(stats),
        axisLabel: {
          inside: false,
          color: '#fff'
        },
        axisTick: {
          show: false
        },
        axisLine: {
          show: false
        },
        z: 10
      },
      yAxis: {
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#999'
        }
      },
      dataZoom: [
        {
          type: 'inside'
        }
      ],
      series: [
        {
          type: 'bar',
          showBackground: true,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            }
          },
          data: this._valueForColumnChart(stats)
        }
      ]
    }

    return option
  }

  private _namesForColumnChart(stats: Stats[]) {
    var val = stats.filter(item =>
        (item.rank as unknown) as number <= 10
    ).map(stat => stat.name)
    return val
  }

  private _valueForColumnChart(stats: Stats[]) {
    var val = stats.filter(item =>
      (item.rank as unknown) as number <= 10
    ).map(stat => stat.priceUsd?.toFixed(2))
    return val
  }
}
