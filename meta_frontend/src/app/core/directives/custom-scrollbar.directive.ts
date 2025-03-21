import { Directive, ElementRef, HostListener, inject } from '@angular/core';

@Directive({
  selector: '[appCustomScrollbar]',
  standalone: true
})
export class CustomScrollbarDirective {
  hostElement!: HTMLElement
  private _element = inject(ElementRef)

  @HostListener("mousemove", ["$event"])
  applyCustomScroll(mouseEvent: MouseEvent) {
    this.hostElement = this._element.nativeElement
    const hostElementPosition = this.hostElement?.getBoundingClientRect()
    const rightEdgeWithoutScrollbar = hostElementPosition.right - 10

    if (mouseEvent.clientX >= rightEdgeWithoutScrollbar) {
      this.hostElement?.classList.add("custom-scroll-vertical-hover")
    } else {
      this.hostElement?.classList.remove("custom-scroll-vertical-hover")
    }
  }

  @HostListener("mouseout")
  removeCustomScroll() {
    this.hostElement?.classList.remove("custom-scroll-vertical-hover")
  }
}
