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
    CommonModule
  ],
  templateUrl: './home-screen.component.html',
  styleUrl: './home-screen.component.scss'
})
export class HomeScreenComponent {

  currentFile?: File;
  fileName = 'Select a File';

  constructor() {

  }

  fileChanged(event: any): void {
    if (event.target.files && event.target.files[0]) {
      const file: File = event.target.files[0];
      this.currentFile = file;
      this.fileName = this.currentFile.name;
    } else {
      this.fileName = 'Select File';
    }
  }


  ngOnDestroy(): void {
  }

}
