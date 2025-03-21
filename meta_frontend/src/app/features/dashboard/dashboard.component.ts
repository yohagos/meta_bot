import { AfterViewInit, Component, inject, OnDestroy, ViewChild } from '@angular/core';
import { SocketService } from './services/socket.service';
import { Stats } from '../../services/models';
import { CommonModule } from '@angular/common';

import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from "@angular/material/input";
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { TextFormatPipe } from '../../core/pipes/text-format.pipe';
import { InterestService } from '../interests/services/interest.service';

@Component({
  selector: 'app-dashboard',
  imports: [
    CommonModule,

    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSortModule,
    MatProgressSpinnerModule,

    TextFormatPipe,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnDestroy, AfterViewInit {
  loading = true
  private _socketService = inject(SocketService)
  private _interestedCoinService = inject(InterestService)

  private currentStat = new Map<string, Stats>()

  displayColumns = ['rank', 'data_id', 'name', 'symbol']
  displayColumnsExtra = [...this.displayColumns, 'expand']
  dataSource = new MatTableDataSource<Stats>([])

  @ViewChild(MatSort) sort!: MatSort

  expandedElementId!: string | null

  constructor() {
    this._socketService.wsSubject$.subscribe((data) => {
      this.handleNewData(data)
    })
  }

  ngAfterViewInit(): void {
      this.dataSource.sort = this.sort
  }


  applyFilter(event: Event) {
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

  private handleNewData(stats: Stats[]) {
    const changes = this.detectChanges(stats)

    if (changes.newEntries.length > 0 || changes.updateEntries.length > 0) {
      this.dataSource.data = this.getSortedData()
    }

    this.loading = false
  }

  private detectChanges(stats: Stats[]): {
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

  private highlightChanges(changes: { newEntries: Stats[], updatedEntries: Stats[] }) {
    changes.newEntries.forEach(stat =>
      this.animateElement(stat.data_id, 'new-entry'));

    changes.updatedEntries.forEach(stat =>
      this.animateElement(stat.data_id, 'rank-changed'));
  }

  private animateElement(coinId: string, animationClass: string) {
    const element = document.getElementById(coinId);
    if (element) {
      element.classList.add(animationClass);
      setTimeout(() =>
        element.classList.remove(animationClass), 1000);
    }
  }

  addToInterested(element: Stats) {
    this._interestedCoinService.addStatsCoin(element)
  }

  ngOnDestroy(): void {
      this._socketService.disconnect()
  }

}
