import { Component } from '@angular/core';
import {Router, RouterOutlet} from '@angular/router';
import {NbLayoutModule} from "@nebular/theme";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NbLayoutModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'frontend';

  constructor(private router: Router) {


  }


  ngOnInit(): void {
      // this.router.events.subscribe((event) => {
      //     document.body.classList.remove('nb-theme-corporate');
      // });
  }
}
