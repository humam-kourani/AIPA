import {Component, Inject, NgZone, ViewChild} from '@angular/core';
import {
  MatDialogModule,
  MAT_DIALOG_DATA,
  MatDialogTitle,
  MatDialogContent, MatDialogActions,
} from '@angular/material/dialog';
import {MatButtonModule} from "@angular/material/button";
import {MatFormField, MatFormFieldModule} from "@angular/material/form-field";
import {CdkTextareaAutosize, TextFieldModule} from "@angular/cdk/text-field";
import {MatSelectModule} from "@angular/material/select";
import {MatInputModule} from "@angular/material/input";
import {MatIcon} from "@angular/material/icon";

export class ApplicationError{
  title: string | undefined
  message: string | undefined;

  constructor(title: string | undefined, message: string | undefined) {
    this.title = title
    this.message = message
  }
}

export interface ErrorDialogData {
  error: any | ApplicationError
}

@Component({
  selector: 'app-error-dialog',
  standalone: true,
  imports: [
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogModule,
    MatButtonModule,
    MatFormField,
    CdkTextareaAutosize,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    TextFieldModule,
    MatIcon
  ],
  templateUrl: './error-dialog.component.html',
  styleUrl: './error-dialog.component.scss'
})
export class ErrorDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: ErrorDialogData) {}

  // example for showing a custom error: this.errorHandlingService.showErrorDialog(new ApplicationError('This is a title', 'This is a message'))
}
