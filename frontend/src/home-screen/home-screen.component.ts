import {ChangeDetectorRef, Component} from '@angular/core';
import {MatButton, MatButtonModule, MatIconButton} from '@angular/material/button';
import {MatDrawer, MatDrawerContainer, MatSidenavContainer, MatSidenavModule} from '@angular/material/sidenav';
import {MediaMatcher} from "@angular/cdk/layout";
import {MatToolbar} from "@angular/material/toolbar";
import {MatListItem, MatListModule, MatNavList} from "@angular/material/list";
import {MatIcon} from "@angular/material/icon";
import {OpenaiConfigurationComponent} from "../openai-configuration/openai-configuration.component";
import {MatCard} from "@angular/material/card";
import {MatFormField, MatFormFieldModule} from "@angular/material/form-field";
import {Observable} from "rxjs";
import {HttpEventType, HttpResponse} from "@angular/common/http";
import {MatInputModule} from "@angular/material/input";
import {CommonModule} from "@angular/common";
import {BackendConnectionService} from "../services/backend-connection.service";
import {ErrorHandlingService} from "../error-dialog/error-handling.service";
import {MatGridList, MatGridTile} from "@angular/material/grid-list";
import {BpmnRendererComponent} from "../bpmn-renderer/bpmn-renderer.component";

@Component({
  selector: 'app-home-screen',
  standalone: true,
  imports: [
    MatDrawer,
    MatSidenavModule,
    MatDrawerContainer,
    MatSidenavContainer,
    MatToolbar,
    MatNavList,
    MatIcon,
    MatButtonModule,
    MatIconButton,
    MatListItem,
    OpenaiConfigurationComponent,
    MatButton,
    MatCard,
    MatFormFieldModule,
    MatInputModule,
    MatListModule,
    CommonModule,
    MatGridList,
    MatGridTile,
    BpmnRendererComponent
  ],
  templateUrl: './home-screen.component.html',
  styleUrl: './home-screen.component.scss'
})
export class HomeScreenComponent {

  currentFile?: File;
  fileName = 'Select a File';
  bpmnContentBase64: string = ''

  constructor(private backendConnectionService: BackendConnectionService,
              private errorHandlingService: ErrorHandlingService) {

  }

  fileChanged(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const file: File = event.target.files[0];

      this.backendConnectionService.uploadBPMN(file).subscribe({
        next: (data: any) => {
          if (data.success && data.bpmn_content_base64){
            this.bpmnContentBase64 = data.bpmn_content_base64
          }
          this.currentFile = file;
          this.fileName = this.currentFile.name;
        },
        error: error => {
          this.errorHandlingService.showErrorDialog(error)
        }
    })
    } else {
      this.fileName = 'Select File';
    }
  }


  ngOnDestroy(): void {
  }

}
