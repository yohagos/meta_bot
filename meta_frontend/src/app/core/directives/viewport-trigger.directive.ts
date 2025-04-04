import { Directive, ElementRef, OnDestroy } from '@angular/core';

@Directive({
  selector: '[appViewportTrigger]',
  standalone: true
})
export class ViewportTriggerDirective implements OnDestroy {
  private observer: IntersectionObserver

  constructor(
    private el: ElementRef
  ) {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        entry.target.classList.toggle('visible', entry.isIntersecting)
      })
    }, {
      threshold: 0.25,
      rootMargin: '0px 0px -100px 0px'
    })
    this.observer.observe(this.el.nativeElement)
  }

  ngOnDestroy() {
    this.observer.disconnect()
  }
}
