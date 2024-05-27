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
import {MatIcon} from "@angular/material/icon";
import {MatTooltipModule} from "@angular/material/tooltip";


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
    MatAutocompleteModule,
    MatTooltipModule,
    MatIcon
  ],
  templateUrl: './openai-configuration.component.html',
  styleUrl: './openai-configuration.component.scss'
})
export class OpenaiConfigurationComponent {

  @Output() closeOverlay = new EventEmitter<boolean>();

  options = ['gpt-3.5-turbo', 'gpt-4-turbo']

  openAIConfigurationForm = this.formBuilder.group({
    modelName: ['', Validators.required],
    apiKey: ['', Validators.required],
    apiURL: ['https://api.openai.com/v1/', Validators.required],
    azureEndpoint: ['']
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
    let azureEndpoint = this.openAIConfigurationForm.get('azureEndpoint')?.value

    this.backendConnectionService.updateConfig(modelName?.toString(), apiKey?.toString(), apiURL?.toString(), azureEndpoint?.toString()).subscribe({
        next: data => {
            localStorage.setItem('model_name', <string>modelName);
            localStorage.setItem('api_key', <string>apiKey);
            localStorage.setItem('api_url', <string>apiURL);
            localStorage.setItem('azure_endpoint', <string>azureEndpoint);

            this.closeOverlay.emit(true)
        },
        error: error => {
          this.errorHandlingService.showErrorDialog(error)
        }
    })
  }



}
