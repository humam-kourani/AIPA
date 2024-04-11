import {Component, EventEmitter, Output} from '@angular/core';
import {FormBuilder, NonNullableFormBuilder, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatFormField} from "@angular/material/form-field";
import {MatOption, MatSelect} from "@angular/material/select";
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatInputModule} from "@angular/material/input";
import {MatButton} from "@angular/material/button";
import {BackendConnectionService} from "../services/backend-connection.service";
import {tap} from "rxjs";
import {ErrorHandlingService} from "../error-dialog/error-handling.service";
import {ApplicationError} from "../error-dialog/error-dialog.component";


@Component({
  selector: 'app-openai-configuration',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatFormField,
    MatSelect,
    MatOption,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButton
  ],
  templateUrl: './openai-configuration.component.html',
  styleUrl: './openai-configuration.component.scss'
})
export class OpenaiConfigurationComponent {

  @Output() closeOverlay = new EventEmitter<boolean>();

  openAIConfigurationForm = this.formBuilder.group({
    modelName: ['', Validators.required],
    apiKey: ['', Validators.required]
  });

  constructor(
    private formBuilder: NonNullableFormBuilder,
    private backendConnectionService: BackendConnectionService,
    private errorHandlingService: ErrorHandlingService
  ) {}


  onSubmit(): void {
    let modelName = this.openAIConfigurationForm.get('modelName')?.value
    let apiKey = this.openAIConfigurationForm.get('apiKey')?.value

    this.backendConnectionService.updateConfig(modelName?.toString(), apiKey?.toString()).subscribe({
        next: data => {
            this.closeOverlay.emit(true)
        },
        error: error => {
          this.errorHandlingService.showErrorDialog(error)
        }
    })
  }



}
