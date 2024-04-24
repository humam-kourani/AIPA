import {Component, EventEmitter, Output} from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatFormField} from "@angular/material/form-field";
import {MatOption, MatSelect} from "@angular/material/select";
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatInputModule} from "@angular/material/input";
import {MatButton} from "@angular/material/button";
import {BackendConnectionService} from "../services/backend-connection.service";
import {ErrorHandlingService} from "../error-dialog/error-handling.service";
import {MatAutocomplete, MatAutocompleteModule} from "@angular/material/autocomplete";


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
    MatButton,
    MatAutocompleteModule
  ],
  templateUrl: './openai-configuration.component.html',
  styleUrl: './openai-configuration.component.scss'
})
export class OpenaiConfigurationComponent {

  @Output() closeOverlay = new EventEmitter<boolean>();

  options = ['gpt-1-turbo-preview', 'gpt-2-turbo-preview', 'gpt-3-turbo-preview', 'gpt-4-turbo-preview']

  openAIConfigurationForm = this.formBuilder.group({
    modelName: ['', Validators.required],
    apiKey: ['', Validators.required],
    apiURL: ['https://api.openai.com/v1/', Validators.required]
  });

  constructor(
    private formBuilder: NonNullableFormBuilder,
    private backendConnectionService: BackendConnectionService,
    private errorHandlingService: ErrorHandlingService
  ) {}


  onSubmit(): void {
    let modelName = this.openAIConfigurationForm.get('modelName')?.value
    let apiKey = this.openAIConfigurationForm.get('apiKey')?.value
    let apiURL = this.openAIConfigurationForm.get('apiURL')?.value

    this.backendConnectionService.updateConfig(modelName?.toString(), apiKey?.toString(), apiURL?.toString()).subscribe({
        next: data => {
            localStorage.setItem('model_name', <string>modelName);
            localStorage.setItem('api_key', <string>apiKey);
            localStorage.setItem('api_url', <string>apiURL);
            this.closeOverlay.emit(true)
        },
        error: error => {
          this.errorHandlingService.showErrorDialog(error)
        }
    })
  }



}
