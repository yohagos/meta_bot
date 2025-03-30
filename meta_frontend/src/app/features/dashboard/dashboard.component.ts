import { AfterViewInit, Component, inject, OnDestroy, ViewChild } from '@angular/core';
import { SocketService } from './services/socket.service';
import { Stats, TransactionRead } from '../../services/models';
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
import { CategoryService } from './services/category.service';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { map, of } from 'rxjs';
import { Router, RouterModule } from '@angular/router';

type Navigation = {
  category: string
  uri: string
}

@Component({
  selector: 'app-dashboard',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,

    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatSelectModule,
    MatSortModule,
    MatProgressSpinnerModule,

    TextFormatPipe
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  private _categoryService = inject(CategoryService)
  private _router = inject(Router)

  navigation: Navigation[] = [
    {
      category: 'all',
      uri: 'dashboard'
    },
    {
      category: 'transactions',
      uri: 'dashboard/transactions'
    },
    {
      category: 'coins',
      uri: 'dashboard/stats'
    },
  ]

  categories$ = this._categoryService.getCategories()

  categoryChanges(event: Event) {
    const category = event as unknown
    const result = (category as string).toLowerCase()
    const uri = this.navigation.find(item => item.category === result)?.uri
    if (uri) this._router.navigate([`${uri}`])
  }

}
