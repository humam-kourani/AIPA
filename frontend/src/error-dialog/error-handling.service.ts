import { Injectable } from '@angular/core';
import {MatDialog} from "@angular/material/dialog";
import {ErrorDialogComponent} from "./error-dialog.component";

@Injectable({
  providedIn: 'root'
})
export class ErrorHandlingService {

  constructor(public dialog: MatDialog) { }

  showErrorDialog(error: any) {
    const dialogRef = this.dialog.open(ErrorDialogComponent, {
      data: {
        error: error,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
