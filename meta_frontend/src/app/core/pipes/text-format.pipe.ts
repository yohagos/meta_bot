import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'textFormat'
})
export class TextFormatPipe implements PipeTransform {

  transform(value: string): string {
    if (value==undefined) return '';
    let preparedResult = value.split('_')
    let result: string = ''
    for (let txt of preparedResult) {
      result += txt.charAt(0).toUpperCase() + txt.substring(1, txt.length + 1).toLowerCase() + ' '
    }
    return result.trim()
  }

}
