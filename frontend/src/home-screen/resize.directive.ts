import { Directive, Input, HostListener, ElementRef } from '@angular/core';

@Directive({
  selector: '[appResize]',
  standalone: true
})
export class ResizeDirective {

  @Input('leftResize') leftElement: HTMLElement | undefined;
  @Input('rightResize') rightElement: HTMLElement | undefined;
  grabber: boolean = false;
  width: number | undefined;
  constructor(private el: ElementRef<HTMLElement>) { }
  @HostListener('window:resize', ['$event']) onResize(event: any) {
    this.width = event.target.outerWidth;
  }
  @HostListener('mousedown') onMouseDown() {
    this.grabber = true;
    this.el.nativeElement.classList.add('side-panel');
    document.body.style.cursor = 'e-resize';
  }

  @HostListener('window:mouseup') onMouseUp() {
    this.grabber = false;
    this.el.nativeElement.classList.remove('side-panel');
    document.body.style.cursor = 'default';
  }

  @HostListener('window:mousemove', ['$event']) onMouseMove(event: MouseEvent) {
    if (this.grabber) {
      event.preventDefault();
      let movementX = event.movementX * 1.1;
      let minWidth = 0.3 * window.screen.width

      // @ts-ignore
      if (this.rightElement?.style.flex !== '' && ((movementX > 0 && Number(this.rightElement.style.flex.split(' ')[2].slice(0, -2)) > minWidth) || (movementX < 0 && Number(this.leftElement.style.flex.split(' ')[2].slice(0, -2)) > minWidth))
      ) {
        // @ts-ignore
        this.rightElement.style.flex = `0 5 ${Number(this.rightElement.style.flex.split(' ')[2].slice(0, -2)) - (movementX)}px`;
        // @ts-ignore
        this.leftElement.style.flex = `1 5 ${Number(this.leftElement.style.flex.split(' ')[2].slice(0, -2)) + (movementX)}px`;
      } else if (this.rightElement?.style.flex === ''){
        // @ts-ignore
        this.leftElement.style.flex = `0 5 ${(event.clientX)}px`;
        // @ts-ignore
        this.rightElement.style.flex = `1 5 ${(event.clientX)}px`;
      }
    }
  }
}
