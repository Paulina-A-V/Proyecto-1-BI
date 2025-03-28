import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FakeNewsService {
  private apiUrl = 'http://localhost:8000';  // Cambia si tu API está en otro puerto

  constructor(private http: HttpClient) {}

  predict(text: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/predict`, { text });
  }
}
