import { AfterContentChecked, AfterViewChecked, AfterViewInit, Component, inject, ViewChild } from '@angular/core';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { Stats } from '../../../services/models';
import { InterestService } from '../../interests/services/interest.service';
import { CategoryService } from '../services/category.service';
import { SocketService } from '../services/socket.service';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { TextFormatPipe } from '../../../core/pipes/text-format.pipe';
import { ColumnChartService } from '../../../shared/services/columnChart/column-chart.service';
import { BehaviorSubject } from 'rxjs';
import { NgxEchartsModule } from 'ngx-echarts';

@Component({
  selector: 'app-stats-board',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,

    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSelectModule,
    MatSortModule,
    MatProgressSpinnerModule,

    NgxEchartsModule,

    TextFormatPipe,
  ],
  templateUrl: './stats-board.component.html',
  styleUrl: './stats-board.component.scss'
})
export class StatsBoardComponent implements AfterContentChecked {
  statsLoading = true
  transactionsLoading = false
  private _categoryService = inject(CategoryService)
  private _socketService = inject(SocketService)
  private _interestedCoinService = inject(InterestService)
  private _columnChartService = inject(ColumnChartService)

  categories$ = this._categoryService.getCategories()
  categorySelected: string = ''

  private currentStat = new Map<string, Stats>()

  displayColumns = ['rank', 'data_id', 'name', 'symbol']
  displayColumnsExtra = [...this.displayColumns, 'expand']
  dataSource = new MatTableDataSource<Stats>([])

  @ViewChild(MatSort) sort!: MatSort

  expandedElementId!: string | null

  statsBarChart: any

  private _switchView = new BehaviorSubject<boolean>(true)
  switchView$ = this._switchView.asObservable()

  constructor() {}

  ngAfterContentChecked(): void {
    this._socketService.stats$.subscribe((data) => {
      this.handleStatsData(data)

      this.statsBarChart = this._columnChartService.createColumnChartWithGradient(data)
    })
  }

  applyStatsFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value
    this.dataSource.filter = filterValue.trim().toLowerCase()

    this.dataSource.filterPredicate = (data: Stats, filter: string) => {
      return data.name.toLowerCase().includes(filter) ||
              data.data_id.toLowerCase().includes(filter) ||
              data.symbol.toLowerCase().includes(filter)
    }
  }

  toggleElement(element: Stats) {
    this.expandedElementId = this.isExpanded(element) ? null : element.data_id
  }

  isExpanded(element: Stats) {
    return this.expandedElementId === element.data_id
  }

  private handleStatsData(stats: Stats[]) {
    const changes = this.detectStatsChanges(stats)

    if (changes.newEntries.length > 0 || changes.updateEntries.length > 0) {
      this.dataSource.data = this.getSortedData()
    }
    this.statsLoading = false
  }

  private detectStatsChanges(stats: Stats[]): {
    newEntries: Stats[],
    updateEntries: Stats[]
  } {
    const result: {
      newEntries: Stats[],
      updateEntries: Stats[]
    } = {
      newEntries: [],
      updateEntries: []
    }

    for (const stat of stats) {
      const existing = this.currentStat.get(stat.data_id)
      if (!existing) {
        result.newEntries.push(stat)
        this.currentStat.set(stat.data_id, stat)
      } else if (existing.rank !== stat.rank) {
        result.updateEntries.push(stat)
        this.currentStat.set(stat.data_id, stat)
      }
    }

    return result
  }

  private getSortedData() {
    return Array.from(this.currentStat.values())
      .sort((a: Stats, b: Stats) => Number(a.rank)  - Number(b.rank))
  }

  switchView() {
    var view = this._switchView.value
    this._switchView.next(!view)
  }

  addToInterested(element: Stats) {
    this._interestedCoinService.addStatsCoin(element)
    this._interestedCoinService.getInterests()
  }

  checkExistenceInInterests(element: Stats) {
    return this._interestedCoinService.checkExistence(element)
  }

  removeFromInterested(element: Stats) {
    this._interestedCoinService.removeInterestById(element)
  }
}
