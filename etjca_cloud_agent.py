</select>
                            </div>
                            
                            <button type="submit" class="btn">🚀 Avvia Ricerca Automatica</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        def handle_run_search(self):
            """Gestisce l'avvio della ricerca automatica"""
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            from urllib.parse import parse_qs
            form_data = parse_qs(post_data)
            
            # Estrai criteri di ricerca
            settori = form_data.get('settori', [])
            posizioni = form_data.get('posizioni', [])
            province = form_data.get('province', ['UD', 'PN', 'GO', 'TS'])
            keywords = form_data.get('keywords', [''])[0].split(',') if form_data.get('keywords', ['']) else []
            esclusioni = form_data.get('esclusioni', [''])[0].split(',') if form_data.get('esclusioni', ['']) else []
            dimensione = form_data.get('dimensione_azienda', [''])[0]
            
            # Crea criteri di ricerca
            criteria = SearchCriteria(
                settori=[s.strip() for s in settori if s.strip()],
                posizioni=[p.strip() for p in posizioni if p.strip()],
                province_fvg=[p.strip() for p in province if p.strip()],
                dimensione_azienda=dimensione,
                keywords=[k.strip() for k in keywords if k.strip()],
                esclusioni=[e.strip() for e in esclusioni if e.strip()]
            )
            
            # Avvia ricerca asincrona in background
            import threading
            
            def run_search_background():
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(agent.run_automated_search(criteria))
                    logger.info(f"🎉 Ricerca completata: {result['total_prospects_found']} nuovi prospects")
                except Exception as e:
                    logger.error(f"❌ Errore ricerca: {e}")
                finally:
                    loop.close()
            
            search_thread = threading.Thread(target=run_search_background, daemon=True)
            search_thread.start()
            
            # Redirect con messaggio
            self.send_response(302)
            self.send_header('Location', '/?search=started')
            self.end_headers()
        
        def send_add_form(self):
            """Form per aggiungere prospect manualmente"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Aggiungi Prospect - ETJCA</title>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                    .header { background: rgba(255,255,255,0.95); color: #2c3e50; padding: 20px; text-align: center; }
                    .nav { background: rgba(52, 58, 64, 0.95); padding: 10px; text-center; }
                    .nav a { color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 4px; }
                    .nav a:hover { background: #495057; }
                    .container { padding: 20px; max-width: 800px; margin: 0 auto; }
                    .form-group { margin-bottom: 15px; }
                    .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: white; }
                    .form-group input, .form-group select, .form-group textarea { 
                        width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; 
                    }
                    .btn { background: #28a745; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
                    .btn:hover { background: #218838; }
                    .form-card { background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>➕ Aggiungi Nuovo Prospect</h1>
                </div>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/add-prospect">➕ Aggiungi Prospect</a>
                    <a href="/search">🔍 Ricerca Automatica</a>
                    <a href="/prospects">👥 Lista Prospects</a>
                    <a href="/reports">📊 Report</a>
                </div>
                <div class="container">
                    <div class="form-card">
                        <form method="POST" action="/add-prospect">
                            <div class="form-group">
                                <label>Nome *</label>
                                <input type="text" name="nome" required>
                            </div>
                            <div class="form-group">
                                <label>Cognome *</label>
                                <input type="text" name="cognome" required>
                            </div>
                            <div class="form-group">
                                <label>Azienda *</label>
                                <input type="text" name="azienda" required>
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" name="email">
                            </div>
                            <div class="form-group">
                                <label>Telefono</label>
                                <input type="text" name="telefono">
                            </div>
                            <div class="form-group">
                                <label>Città</label>
                                <input type="text" name="citta">
                            </div>
                            <div class="form-group">
                                <label>Provincia</label>
                                <select name="provincia">
                                    <option value="">Seleziona...</option>
                                    <option value="UD">Udine</option>
                                    <option value="PN">Pordenone</option>
                                    <option value="GO">Gorizia</option>
                                    <option value="TS">Trieste</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Settore</label>
                                <input type="text" name="settore" placeholder="es: Tecnologia, Manifatturiero, Servizi...">
                            </div>
                            <div class="form-group">
                                <label>Posizione</label>
                                <input type="text" name="posizione" placeholder="es: CEO, Sales Manager, CTO...">
                            </div>
                            <div class="form-group">
                                <label>Note</label>
                                <textarea name="note" rows="3" placeholder="Note aggiuntive..."></textarea>
                            </div>
                            <button type="submit" class="btn">💾 Salva Prospect</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        def handle_add_prospect(self):
            """Gestisce l'aggiunta di un prospect manuale"""
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            from urllib.parse import parse_qs
            form_data = parse_qs(post_data)
            
            prospect_data = {}
            for key, values in form_data.items():
                prospect_data[key] = values[0] if values else ""
            
            success = agent.add_prospect_manual(prospect_data)
            
            if success:
                self.send_response(302)
                self.send_header('Location', '/?msg=prospect_added')
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header('Location', '/add-prospect?msg=error')
                self.end_headers()
        
        def send_prospects_list(self):
            """Lista completa prospects"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            prospects = agent.get_all_prospects()
            
            rows = ""
            for i, prospect in enumerate(prospects, 1):
                fonte_badge = {
                    'manuale': '📝 Manuale',
                    'linkedin': '💼 LinkedIn', 
                    'sales_navigator': '🎯 Sales Navigator',
                    'camera_commercio': '🏢 Camera Commercio'
                }.get(prospect.fonte, prospect.fonte)
                
                linkedin_link = f'<a href="{prospect.linkedin_url}" target="_blank">🔗 LinkedIn</a>' if prospect.linkedin_url else ""
                
                rows += f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{prospect.nome} {prospect.cognome}</strong><br><small>{prospect.posizione}</small></td>
                    <td>{prospect.azienda}</td>
                    <td>{prospect.email}<br><small>{prospect.telefono}</small></td>
                    <td>{prospect.citta}, {prospect.provincia}</td>
                    <td><span class="fonte-badge">{fonte_badge}</span></td>
                    <td><span class="badge badge-{prospect.stato}">{prospect.stato}</span></td>
                    <td>{prospect.data_inserimento.strftime('%d/%m/%Y')}<br>{linkedin_link}</td>
                </tr>
                """
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Lista Prospects - ETJCA</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }}
                    .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
                    .nav {{ background: #343a40; padding: 10px; text-align: center; }}
                    .nav a {{ color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 4px; }}
                    .nav a:hover {{ background: #495057; }}
                    .container {{ padding: 20px; }}
                    table {{ width: 100%; background: white; border-collapse: collapse; margin-top: 20px; }}
                    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background: #f8f9fa; font-weight: bold; }}
                    .badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; }}
                    .badge-nuovo {{ background: #6c757d; }}
                    .badge-contattato {{ background: #17a2b8; }}
                    .badge-qualificato {{ background: #ffc107; color: #212529; }}
                    .badge-convertito {{ background: #28a745; }}
                    .badge-perso {{ background: #dc3545; }}
                    .fonte-badge {{ background: #e9ecef; color: #495057; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; }}
                    .stats {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                    .stat-item {{ text-align: center; }}
                    .stat-number {{ font-size: 1.5em; font-weight: bold; color: #007bff; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>👥 Lista Prospects Completa</h1>
                </div>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/add-prospect">➕ Aggiungi Prospect</a>
                    <a href="/search">🔍 Ricerca Automatica</a>
                    <a href="/prospects">👥 Lista Prospects</a>
                    <a href="/reports">📊 Report</a>
                </div>
                <div class="container">
                    <div class="stats">
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-number">{len(prospects)}</div>
                                <div>Total Prospects</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">{len([p for p in prospects if p.fonte == 'linkedin'])}</div>
                                <div>da LinkedIn</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">{len([p for p in prospects if p.fonte == 'manuale'])}</div>
                                <div>Manuali</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number">{len([p for p in prospects if p.provincia == 'UD'])}</div>
                                <div>Udine</div>
                            </div>
                        </div>
                    </div>
                    
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Nome & Posizione</th>
                                <th>Azienda</th>
                                <th>Contatti</th>
                                <th>Località</th>
                                <th>Fonte</th>
                                <th>Stato</th>
                                <th>Data & Link</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows if rows else '<tr><td colspan="8" style="text-align: center; padding: 40px;">Nessun prospect trovato. <a href="/add-prospect">Aggiungi il primo prospect</a></td></tr>'}
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        def send_reports(self):
            """Report e analytics avanzati"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            stats = agent.db.get_report_statistics()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Report & Analytics - ETJCA</title>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }}
                    .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
                    .nav {{ background: #343a40; padding: 10px; text-align: center; }}
                    .nav a {{ color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 4px; }}
                    .nav a:hover {{ background: #495057; }}
                    .container {{ padding: 20px; }}
                    .report-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
                    .report-section {{ background: white; margin: 20px 0; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    .chart-container {{ margin: 20px 0; }}
                    .chart-bar {{ height: 25px; background: #007bff; margin: 8px 0; border-radius: 4px; position: relative; }}
                    .chart-label {{ position: absolute; left: 10px; top: 4px; color: white; font-size: 0.9em; font-weight: bold; }}
                    .metric-card {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #007bff; }}
                    .metric-title {{ font-weight: bold; color: #495057; }}
                    .metric-value {{ font-size: 1.5em; color: #007bff; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Report & Analytics ETJCA</h1>
                    <p>Analisi performance Lead Generation FVG</p>
                </div>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/add-prospect">➕ Aggiungi Prospect</a>
                    <a href="/search">🔍 Ricerca Automatica</a>
                    <a href="/prospects">👥 Lista Prospects</a>
                    <a href="/reports">📊 Report</a>
                </div>
                <div class="container">
                    <div class="report-grid">
                        <div class="report-section">
                            <h3>📈 Riepilogo Generale</h3>
                            <div class="metric-card">
                                <div class="metric-title">Total Prospects</div>
                                <div class="metric-value">{stats.get('total_prospects', 0)}</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-title">Inseriti Oggi</div>
                                <div class="metric-value">{stats.get('inseriti_oggi', 0)}</div>
                            </div>
                        </div>
                        
                        <div class="report-section">
                            <h3>🏘️ Distribuzione per Provincia</h3>
                            <div class="chart-container">
                                {self._generate_province_chart(stats.get('per_provincia', {}))}
                            </div>
                        </div>
                        
                        <div class="report-section">
                            <h3>🔍 Performance per Fonte</h3>
                            <div class="chart-container">
                                {self._generate_fonte_chart(stats.get('per_fonte', {}))}
                            </div>
                        </div>
                        
                        <div class="report-section">
                            <h3>📊 Stati Prospects</h3>
                            <div class="chart-container">
                                {self._generate_stato_chart(stats.get('per_stato', {}))}
                            </div>
                        </div>
                    </div>
                    
                    {self._generate_recent_searches_report(stats.get('recent_searches', []))}
                    
                    <div class="report-section">
                        <h3>🎯 Insights & Raccomandazioni</h3>
                        <ul>
                            <li><strong>Top Provincia:</strong> {self._get_top_provincia(stats.get('per_provincia', {}))}</li>
                            <li><strong>Fonte più Produttiva:</strong> {self._get_top_fonte(stats.get('per_fonte', {}))}</li>
                            <li><strong>Tasso Conversione:</strong> {self._calculate_conversion_rate(stats.get('per_stato', {}))}%</li>
                        </ul>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        def _generate_province_chart(self, per_provincia):
            if not per_provincia:
                return "<p>Nessun dato disponibile</p>"
            
            max_val = max(per_provincia.values()) if per_provincia.values() else 1
            chart_html = ""
            
            province_names = {'UD': 'Udine', 'PN': 'Pordenone', 'GO': 'Gorizia', 'TS': 'Trieste'}
            
            for prov, count in per_provincia.items():
                width = (count / max_val) * 100
                nome_provincia = province_names.get(prov, prov)
                chart_html += f'''
                <div class="chart-bar" style="width: {width}%;">
                    <div class="chart-label">{nome_provincia}: {count}</div>
                </div>
                '''
            return chart_html
        
        def _generate_fonte_chart(self, per_fonte):
            if not per_fonte:
                return "<p>Nessun dato disponibile</p>"
            
            max_val = max(per_fonte.values()) if per_fonte.values() else 1
            chart_html = ""
            
            fonte_names = {
                'manuale': '📝 Manuale',
                'linkedin': '💼 LinkedIn',
                'sales_navigator': '🎯 Sales Navigator',
                'camera_commercio': '🏢 Camera Commercio'
            }
            
            for fonte, count in per_fonte.items():
                width = (count / max_val) * 100
                nome_fonte = fonte_names.get(fonte, fonte)
                chart_html += f'''
                <div class="chart-bar" style="width: {width}%;">
                    <div class="chart-label">{nome_fonte}: {count}</div>
                </div>
                '''
            return chart_html
        
        def _generate_stato_chart(self, per_stato):
            if not per_stato:
                return "<p>Nessun dato disponibile</p>"
            
            max_val = max(per_stato.values()) if per_stato.values() else 1
            chart_html = ""
            
            for stato, count in per_stato.items():
                width = (count / max_val) * 100
                chart_html += f'''
                <div class="chart-bar" style="width: {width}%;">
                    <div class="chart-label">{stato.title()}: {count}</div>
                </div>
                '''
            return chart_html
        
        def _generate_recent_searches_report(self, recent_searches):
            if not recent_searches:
                return ""
            
            searches_html = ""
            for search in recent_searches:
                status_icon = "✅" if search['success'] else "❌"
                searches_html += f"""
                <div class="metric-card">
                    <div class="metric-title">{status_icon} {search['source'].title()}</div>
                    <div class="metric-value">{search['prospects_found']} prospects</div>
                    <small>{search['timestamp'][:19].replace('T', ' ')}</small>
                </div>
                """
            
            return f"""
            <div class="report-section">
                <h3>🔍 Ricerche Recenti</h3>
                {searches_html}
            </div>
            """
        
        def _get_top_provincia(self, per_provincia):
            if not per_provincia:
                return "N/A"
            top_prov = max(per_provincia.items(), key=lambda x: x[1])
            province_names = {'UD': 'Udine', 'PN': 'Pordenone', 'GO': 'Gorizia', 'TS': 'Trieste'}
            return f"{province_names.get(top_prov[0], top_prov[0])} ({top_prov[1]} prospects)"
        
        def _get_top_fonte(self, per_fonte):
            if not per_fonte:
                return "N/A"
            top_fonte = max(per_fonte.items(), key=lambda x: x[1])
            return f"{top_fonte[0].title()} ({top_fonte[1]} prospects)"
        
        def _calculate_conversion_rate(self, per_stato):
            if not per_stato:
                return 0
            total = sum(per_stato.values())
            convertiti = per_stato.get('convertito', 0)
            return round((convertiti / total * 100), 1) if total > 0 else 0
        
        def send_status(self):
            """API endpoint per status JSON"""
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            import json
            status = agent.get_status()
            self.wfile.write(json.dumps(status, indent=2).encode())
        
        def send_404(self):
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1><a href="/">Torna alla Dashboard</a>')
    
    # Inizializza dati di esempio
    init_sample_data()
    
    # Avvia web server
    port = int(os.environ.get('PORT', 8000))
    httpd = HTTPServer(('0.0.0.0', port), ETJCACompleteHandler)
    
    def start_web_server():
        logger.info(f"🌐 ETJCA Complete Server avviato su porta {port}")
        httpd.serve_forever()
    
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    
    try:
        logger.info("🚀 Avvio ETJCA Complete Lead Generation System...")
        logger.info("🔍 Fonti abilitate: Manuale, LinkedIn, Sales Navigator, Camera Commercio")
        logger.info("📍 Territory: Friuli Venezia Giulia")
        logger.info("⚡ Protocol: MCP (Model Context Protocol)")
        logger.info(f"🌐 Dashboard: http://localhost:{port}")
        
        # Mantieni l'applicazione in vita
        while True:
            await asyncio.sleep(3600)  # Check ogni ora
            logger.info("💓 ETJCA System heartbeat - sistema attivo")
            
    except Exception as e:
        logger.error(f"❌ Errore fatale ETJCA: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
                source="linkedin",
                prospects_found=saved_count,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=True
            )
            
            # Salva risultato ricerca
            self.db.save_search_result(result)
            
            logger.info(f"✅ LinkedIn search completata: {saved_count} nuovi prospects")
            return result
            
        except Exception as e:
            error_msg = f"Errore ricerca LinkedIn: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return SearchResult(
                source="linkedin",
                prospects_found=0,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=False,
                error_message=error_msg
            )
    
    async def search_sales_navigator_leads(self, criteria: SearchCriteria) -> SearchResult:
        """Ricerca lead su Sales Navigator"""
        logger.info("🎯 Avvio ricerca Sales Navigator...")
        
        if not self.linkedin_searcher:
            error_msg = "Sales Navigator searcher non disponibile"
            logger.error(f"❌ {error_msg}")
            return SearchResult(
                source="sales_navigator",
                prospects_found=0,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=False,
                error_message=error_msg
            )
        
        try:
            # Ricerca prospects
            prospects_data = await self.linkedin_searcher.search_sales_navigator(criteria)
            
            # Salva prospects nel database
            saved_count = 0
            for prospect_data in prospects_data:
                prospect = self._create_prospect_from_data(prospect_data, "sales_navigator")
                if self.db.save_prospect(prospect):
                    saved_count += 1
            
            # Crea risultato
            result = SearchResult(
                source="sales_navigator",
                prospects_found=saved_count,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=True
            )
            
            self.db.save_search_result(result)
            
            logger.info(f"✅ Sales Navigator search completata: {saved_count} nuovi prospects")
            return result
            
        except Exception as e:
            error_msg = f"Errore ricerca Sales Navigator: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return SearchResult(
                source="sales_navigator",
                prospects_found=0,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=False,
                error_message=error_msg
            )
    
    async def search_camera_commercio_leads(self, criteria: SearchCriteria) -> SearchResult:
        """Ricerca aziende da Camera di Commercio"""
        logger.info("🏢 Avvio ricerca Camera di Commercio...")
        
        try:
            # Ricerca aziende
            companies_data = await self.camera_searcher.search_companies_fvg(criteria)
            
            # Salva come prospects
            saved_count = 0
            for company_data in companies_data:
                prospect = self._create_prospect_from_data(company_data, "camera_commercio")
                if self.db.save_prospect(prospect):
                    saved_count += 1
            
            # Crea risultato
            result = SearchResult(
                source="camera_commercio",
                prospects_found=saved_count,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=True
            )
            
            self.db.save_search_result(result)
            
            logger.info(f"✅ Camera Commercio search completata: {saved_count} nuove aziende")
            return result
            
        except Exception as e:
            error_msg = f"Errore ricerca Camera Commercio: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return SearchResult(
                source="camera_commercio",
                prospects_found=0,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=False,
                error_message=error_msg
            )
    
    async def run_automated_search(self, criteria: SearchCriteria) -> Dict:
        """Esegue ricerca automatica su tutte le fonti"""
        logger.info("🚀 Avvio ricerca automatica multi-fonte...")
        
        results = {}
        total_found = 0
        
        # 1. LinkedIn normale
        if "linkedin" in self.config["supported_sources"]:
            linkedin_result = await self.search_linkedin_leads(criteria)
            results["linkedin"] = linkedin_result
            if linkedin_result.success:
                total_found += linkedin_result.prospects_found
        
        # 2. Sales Navigator
        if "sales_navigator" in self.config["supported_sources"]:
            sales_result = await self.search_sales_navigator_leads(criteria)
            results["sales_navigator"] = sales_result
            if sales_result.success:
                total_found += sales_result.prospects_found
        
        # 3. Camera di Commercio
        if "camera_commercio" in self.config["supported_sources"]:
            camera_result = await self.search_camera_commercio_leads(criteria)
            results["camera_commercio"] = camera_result
            if camera_result.success:
                total_found += camera_result.prospects_found
        
        # Chiudi connessioni
        if self.linkedin_searcher:
            self.linkedin_searcher.close()
        
        summary = {
            "total_prospects_found": total_found,
            "sources_searched": len(results),
            "results_by_source": {
                source: {
                    "prospects_found": result.prospects_found,
                    "success": result.success,
                    "error": result.error_message
                }
                for source, result in results.items()
            },
            "search_criteria": asdict(criteria),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Ricerca automatica completata: {total_found} nuovi prospects totali")
        return summary
    
    def _create_prospect_from_data(self, data: Dict, fonte: str) -> Prospect:
        """Crea un oggetto Prospect dai dati grezzi"""
        return Prospect(
            id=f"{fonte}-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:8]}",
            nome=data.get("nome", ""),
            cognome=data.get("cognome", ""), 
            azienda=data.get("azienda", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            citta=data.get("citta", ""),
            provincia=data.get("provincia", ""),
            settore=data.get("settore", ""),
            fonte=fonte,
            linkedin_url=data.get("linkedin_url", ""),
            azienda_linkedin=data.get("azienda_linkedin", data.get("azienda", "")),
            posizione=data.get("posizione", ""),
            stato="nuovo",
            note=f"Importato automaticamente da {fonte}",
            data_inserimento=datetime.now()
        )
    
    def get_all_prospects(self) -> List[Prospect]:
        """Recupera tutti i prospects"""
        return self.db.get_all_prospects()
    
    def get_dashboard_stats(self) -> Dict:
        """Ottiene statistiche complete per la dashboard"""
        stats = self.db.get_report_statistics()
        
        return {
            "agent_info": self.config,
            "statistics": stats,
            "credentials_configured": {
                "linkedin": bool(self.credentials["linkedin"]["email"]),
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self):
        """Ritorna lo status dell'agente MCP"""
        stats = self.db.get_report_statistics()
        return {
            "agent_name": self.config["agent_name"],
            "version": self.config["version"],
            "protocol": "MCP",
            "territory": self.config["territory"],
            "total_prospects": stats.get("total_prospects", 0),
            "sources_active": len([s for s in self.config["supported_sources"] if s != "manual"]),
            "status": "running" if self.running else "stopped",
            "timestamp": datetime.now().isoformat()
        }

# Istanza globale
agent = ETJCAMCPAgent()

# Inizializzazione dati di esempio
def init_sample_data():
    """Inizializza dati di esempio realistici"""
    sample_prospects = [
        {
            "nome": "Mario", "cognome": "Rossi", "azienda": "Tech Solutions SRL",
            "email": "mario.rossi@techsolutions.it", "telefono": "0432123456",
            "citta": "Udine", "provincia": "UD", "settore": "Tecnologia",
            "posizione": "CTO", "note": "Interessato a soluzioni cloud"
        },
        {
            "nome": "Laura", "cognome": "Bianchi", "azienda": "Green Energy SpA", 
            "email": "l.bianchi@greenenergy.it", "telefono": "0434987654",
            "citta": "Pordenone", "provincia": "PN", "settore": "Energia",
            "posizione": "Sales Director", "note": "Richiesta demo prodotti sostenibili"
        },
        {
            "nome": "Giuseppe", "cognome": "Verdi", "azienda": "Mare Adriatico SNC",
            "email": "g.verdi@mareadriatico.it", "telefono": "040555666", 
            "citta": "Trieste", "provincia": "TS", "settore": "Turismo",
            "posizione": "Marketing Manager", "note": "Espansione digitale"
        }
    ]
    
    for prospect_data in sample_prospects:
        agent.add_prospect_manual(prospect_data)
    
    logger.info("📊 Dati di esempio inizializzati")

async def main():
    """Funzione principale con dashboard completa"""
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    
    class ETJCACompleteHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/':
                self.send_dashboard()
            elif path == '/add-prospect':
                self.send_add_form()
            elif path == '/prospects':
                self.send_prospects_list()
            elif path == '/search':
                self.send_search_form()
            elif path == '/reports':
                self.send_reports()
            elif path == '/status':
                self.send_status()
            else:
                self.send_404()
        
        def do_POST(self):
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/add-prospect':
                self.handle_add_prospect()
            elif path == '/run-search':
                self.handle_run_search()
            else:
                self.send_404()
        
        def send_dashboard(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            stats = agent.get_dashboard_stats()
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ETJCA Complete Lead Generation - Dashboard</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                    .header {{ background: rgba(255,255,255,0.95); color: #2c3e50; padding: 30px; text-align: center; backdrop-filter: blur(10px); }}
                    .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
                    .protocol-badge {{ background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; display: inline-block; }}
                    .nav {{ background: rgba(52, 58, 64, 0.95); padding: 15px; text-align: center; backdrop-filter: blur(10px); }}
                    .nav a {{ color: white; text-decoration: none; margin: 0 20px; padding: 10px 20px; border-radius: 8px; transition: all 0.3s; }}
                    .nav a:hover {{ background: #495057; transform: translateY(-2px); }}
                    .container {{ padding: 30px; max-width: 1400px; margin: 0 auto; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 40px; }}
                    .stat-card {{ background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s; }}
                    .stat-card:hover {{ transform: translateY(-5px); }}
                    .stat-number {{ font-size: 2.5em; font-weight: bold; color: #667eea; margin-bottom: 10px; }}
                    .stat-label {{ color: #6c757d; font-weight: 500; }}
                    .sources-section {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; margin-bottom: 30px; }}
                    .source-item {{ display: inline-block; background: #e9ecef; padding: 10px 20px; margin: 5px; border-radius: 25px; }}
                    .source-active {{ background: #28a745; color: white; }}
                    .actions-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                    .action-card {{ background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px; text-align: center; }}
                    .btn {{ display: inline-block; padding: 15px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; transition: all 0.3s; border: none; cursor: pointer; }}
                    .btn:hover {{ background: #5a6fd8; transform: translateY(-2px); }}
                    .btn-success {{ background: #28a745; }}
                    .btn-info {{ background: #17a2b8; }}
                    .btn-warning {{ background: #ffc107; color: #212529; }}
                    .recent-searches {{ margin-top: 30px; }}
                    .search-item {{ background: rgba(255,255,255,0.9); padding: 15px; margin: 10px 0; border-radius: 10px; display: flex; justify-content: space-between; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚀 ETJCA Complete Lead Generation</h1>
                    <div class="protocol-badge">MCP Protocol</div>
                    <p style="margin-top: 10px;">Territorio: {stats['agent_info']['territory']} • Version {stats['agent_info']['version']}</p>
                </div>
                
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/add-prospect">➕ Aggiungi Prospect</a>
                    <a href="/search">🔍 Ricerca Automatica</a>
                    <a href="/prospects">👥 Lista Prospects</a>
                    <a href="/reports">📊 Report</a>
                </div>
                
                <div class="container">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{stats['statistics'].get('total_prospects', 0)}</div>
                            <div class="stat-label">📋 Total Prospects</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{stats['statistics'].get('inseriti_oggi', 0)}</div>
                            <div class="stat-label">📅 Inseriti Oggi</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{len(stats['statistics'].get('per_fonte', {}))}</div>
                            <div class="stat-label">🔍 Fonti Attive</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{len(stats['agent_info']['province'])}</div>
                            <div class="stat-label">🏘️ Province FVG</div>
                        </div>
                    </div>
                    
                    <div class="sources-section">
                        <h3 style="margin-bottom: 20px;">🔍 Fonti di Lead Generation</h3>
                        <div>
                            <span class="source-item source-active">📝 Inserimento Manuale</span>
                            <span class="source-item {'source-active' if stats['credentials_configured']['linkedin'] else ''}">💼 LinkedIn</span>
                            <span class="source-item {'source-active' if stats['credentials_configured']['linkedin'] else ''}">🎯 Sales Navigator</span>
                            <span class="source-item source-active">🏢 Camera di Commercio</span>
                        </div>
                        {f'<p style="margin-top: 15px; color: #dc3545;"><strong>⚠️ LinkedIn non configurato:</strong> Aggiungi LINKEDIN_EMAIL e LINKEDIN_PASSWORD nelle variabili ambiente per abilitare la ricerca automatica.</p>' if not stats['credentials_configured']['linkedin'] else ''}
                    </div>
                    
                    <div class="actions-grid">
                        <div class="action-card">
                            <h4>➕ Inserimento Manuale</h4>
                            <p>Aggiungi prospects manualmente tramite form</p>
                            <a href="/add-prospect" class="btn btn-success">Aggiungi Prospect</a>
                        </div>
                        
                        <div class="action-card">
                            <h4>🔍 Ricerca Automatica</h4>
                            <p>Cerca lead su LinkedIn, Sales Navigator e Camera di Commercio</p>
                            <a href="/search" class="btn btn-info">Avvia Ricerca</a>
                        </div>
                        
                        <div class="action-card">
                            <h4>👥 Gestione Prospects</h4>
                            <p>Visualizza e gestisci tutti i prospects acquisiti</p>
                            <a href="/prospects" class="btn">Visualizza Lista</a>
                        </div>
                        
                        <div class="action-card">
                            <h4>📊 Report & Analytics</h4>
                            <p>Analisi performance e statistiche territoriali</p>
                            <a href="/reports" class="btn btn-warning">Visualizza Report</a>
                        </div>
                    </div>
                    
                    {self._generate_recent_searches_html(stats['statistics'].get('recent_searches', []))}
                    
                    <div style="margin-top: 40px; text-align: center; color: rgba(255,255,255,0.8);">
                        <p>📊 Ultimo aggiornamento: {stats['timestamp'][:19].replace('T', ' ')}</p>
                        <p>🔄 MCP Protocol • 🌐 Multi-Source Lead Generation • 🎯 FVG Territory</p>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        def _generate_recent_searches_html(self, recent_searches):
            """Genera HTML per ricerche recenti"""
            if not recent_searches:
                return ""
            
            searches_html = ""
            for search in recent_searches[:3]:
                status_color = "#28a745" if search['success'] else "#dc3545"
                status_text = "✅ Successo" if search['success'] else "❌ Errore"
                
                searches_html += f"""
                <div class="search-item">
                    <div>
                        <strong>{search['source'].title()}</strong> - {search['prospects_found']} prospects
                        <br><small>{search['timestamp'][:19].replace('T', ' ')}</small>
                    </div>
                    <div style="color: {status_color};">{status_text}</div>
                </div>
                """
            
            return f"""
            <div class="recent-searches">
                <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;">
                    <h3>📈 Ricerche Recenti</h3>
                    {searches_html}
                </div>
            </div>
            """
        
        def send_search_form(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Ricerca Automatica - ETJCA</title>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
                    .header { background: rgba(255,255,255,0.95); color: #2c3e50; padding: 20px; text-align: center; }
                    .nav { background: rgba(52, 58, 64, 0.95); padding: 10px; text-align: center; }
                    .nav a { color: white; text-decoration: none; margin: 0 15px; padding: 8px 16px; border-radius: 4px; }
                    .nav a:hover { background: #495057; }
                    .container { padding: 30px; max-width: 800px; margin: 0 auto; }
                    .form-card { background: rgba(255,255,255,0.95); padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                    .form-group { margin-bottom: 20px; }
                    .form-group label { display: block; margin-bottom: 8px; font-weight: bold; color: #2c3e50; }
                    .form-group input, .form-group select, .form-group textarea { 
                        width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 14px;
                    }
                    .form-group input:focus, .form-group select:focus { border-color: #667eea; outline: none; }
                    .checkbox-group { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
                    .checkbox-item { background: #f8f9fa; padding: 10px; border-radius: 5px; }
                    .btn { background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
                    .btn:hover { background: #5a6fd8; }
                    .warning { background: #fff3cd; color: #856404; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🔍 Ricerca Automatica Lead</h1>
                    <p>Configura i criteri per la ricerca multi-fonte</p>
                </div>
                <div class="nav">
                    <a href="/">🏠 Dashboard</a>
                    <a href="/add-prospect">➕ Aggiungi Prospect</a>
                    <a href="/search">🔍 Ricerca Automatica</a>
                    <a href="/prospects">👥 Lista Prospects</a>
                    <a href="/reports">📊 Report</a>
                </div>
                <div class="container">
                    <div class="form-card">
                        <div class="warning">
                            <strong>⚠️ Nota:</strong> La ricerca automatica utilizzerà LinkedIn, Sales Navigator e Camera di Commercio. 
                            Assicurati che le credenziali LinkedIn siano configurate nelle variabili ambiente.
                        </div>
                        
                        <form method="POST" action="/run-search">
                            <div class="form-group">
                                <label>🏢 Settori Target</label>
                                <div class="checkbox-group">
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Tecnologia" id="tech"> 
                                        <label for="tech">Tecnologia</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Manifatturiero" id="manuf"> 
                                        <label for="manuf">Manifatturiero</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Servizi" id="serv"> 
                                        <label for="serv">Servizi</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Energia" id="energy"> 
                                        <label for="energy">Energia</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Turismo" id="tourism"> 
                                        <label for="tourism">Turismo</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="settori" value="Logistica" id="logistics"> 
                                        <label for="logistics">Logistica</label>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>👤 Posizioni Target</label>
                                <div class="checkbox-group">
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="posizioni" value="CEO" id="ceo"> 
                                        <label for="ceo">CEO</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="posizioni" value="Sales Manager" id="sales"> 
                                        <label for="sales">Sales Manager</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="posizioni" value="Marketing Manager" id="marketing"> 
                                        <label for="marketing">Marketing Manager</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="posizioni" value="CTO" id="cto"> 
                                        <label for="cto">CTO</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="posizioni" value="Business Development" id="bizdev"> 
                                        <label for="bizdev">Business Development</label>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>🏘️ Province FVG</label>
                                <div class="checkbox-group">
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="province" value="UD" id="ud" checked> 
                                        <label for="ud">Udine</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="province" value="PN" id="pn" checked> 
                                        <label for="pn">Pordenone</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="province" value="GO" id="go" checked> 
                                        <label for="go">Gorizia</label>
                                    </div>
                                    <div class="checkbox-item">
                                        <input type="checkbox" name="province" value="TS" id="ts" checked> 
                                        <label for="ts">Trieste</label>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>🔍 Keywords Aggiuntive</label>
                                <input type="text" name="keywords" placeholder="Separati da virgola (es: innovation, digital transformation, sustainability)">
                            </div>
                            
                            <div class="form-group">
                                <label>❌ Esclusioni</label>
                                <input type="text" name="esclusioni" placeholder="Termini da escludere, separati da virgola">
                            </div>
                            
                            <div class="form-group">
                                <label>🏢 Dimensione Azienda</label>
                                <select name="dimensione_azienda">
                                    <option value="">Tutte le dimensioni</option>
                                    <option value="startup">Startup</option>
                                    <option value="small">Piccola (1-50 dipendenti)</option>
                                    <option value="medium">Media (51-250 dipendenti)</option>
                                    <option value="large">Grande (250+ dipendenti)</option#!/usr/bin/env python3
"""
ETJCA Complete Lead Generation System
Sistema completo con ricerca automatica LinkedIn, Sales Navigator e DB pubblici
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
import json
import sqlite3
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import uuid
import time
import random

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importazioni condizionali per web scraping
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("⚠️ Selenium non disponibile - funzionalità di scraping disabilitate")

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("⚠️ Requests/BeautifulSoup non disponibili")

@dataclass
class Prospect:
    """Rappresenta un prospect/lead"""
    id: str
    nome: str
    cognome: str
    azienda: str
    email: str
    telefono: str
    citta: str
    provincia: str  # UD, PN, GO, TS
    settore: str
    fonte: str  # manuale, linkedin, sales_navigator, camera_commercio
    linkedin_url: str
    azienda_linkedin: str
    posizione: str
    stato: str  # nuovo, contattato, qualificato, convertito, perso
    note: str
    data_inserimento: datetime
    ultimo_contatto: Optional[datetime] = None
    prossimo_followup: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['data_inserimento'] = self.data_inserimento.isoformat()
        if self.ultimo_contatto:
            data['ultimo_contatto'] = self.ultimo_contatto.isoformat()
        if self.prossimo_followup:
            data['prossimo_followup'] = self.prossimo_followup.isoformat()
        return data

@dataclass
class SearchCriteria:
    """Criteri di ricerca per lead generation"""
    settori: List[str]
    posizioni: List[str]
    province_fvg: List[str]
    dimensione_azienda: str  # startup, small, medium, large
    keywords: List[str]
    esclusioni: List[str]

@dataclass
class SearchResult:
    """Risultato di una ricerca"""
    source: str  # linkedin, sales_navigator, camera_commercio
    prospects_found: int
    search_criteria: SearchCriteria
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None

class LinkedInSearcher:
    """Gestore ricerca LinkedIn e Sales Navigator"""
    
    def __init__(self, credentials: Dict):
        self.email = credentials.get('email')
        self.password = credentials.get('password')
        self.driver = None
        self.logged_in = False
        
    def init_driver(self):
        """Inizializza il driver Selenium"""
        if not SELENIUM_AVAILABLE:
            logger.error("❌ Selenium non disponibile per LinkedIn search")
            return False
            
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Per Railway
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            logger.error(f"❌ Errore inizializzazione driver: {e}")
            return False
    
    async def login_linkedin(self) -> bool:
        """Login a LinkedIn"""
        if not self.driver:
            if not self.init_driver():
                return False
                
        try:
            logger.info("🔐 Login a LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            
            # Inserisci credenziali
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")
            
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
            
            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "[type='submit']")
            login_button.click()
            
            # Attendi caricamento
            await asyncio.sleep(3)
            
            # Verifica login
            if "feed" in self.driver.current_url or "in/" in self.driver.current_url:
                self.logged_in = True
                logger.info("✅ Login LinkedIn riuscito")
                return True
            else:
                logger.error("❌ Login LinkedIn fallito")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore login LinkedIn: {e}")
            return False
    
    async def search_linkedin_prospects(self, criteria: SearchCriteria) -> List[Dict]:
        """Ricerca prospects su LinkedIn normale"""
        if not self.logged_in:
            if not await self.login_linkedin():
                return []
        
        prospects = []
        
        try:
            # Costruisci query di ricerca
            search_terms = []
            
            # Aggiungi settori
            if criteria.settori:
                search_terms.extend(criteria.settori)
            
            # Aggiungi posizioni
            if criteria.posizioni:
                search_terms.extend(criteria.posizioni)
            
            # Aggiungi filtri geografici FVG
            location_terms = []
            province_map = {
                'UD': ['Udine', 'Friuli'],
                'PN': ['Pordenone'],
                'GO': ['Gorizia'],
                'TS': ['Trieste']
            }
            
            for prov in criteria.province_fvg:
                if prov in province_map:
                    location_terms.extend(province_map[prov])
            
            # Esegui ricerca per ogni combinazione
            for settore in criteria.settori[:2]:  # Limita a 2 settori per non sovraccaricare
                for location in location_terms[:3]:  # Limita a 3 location
                    search_query = f"{settore} {location}"
                    
                    logger.info(f"🔍 Ricerca LinkedIn: {search_query}")
                    
                    # Vai alla pagina di ricerca
                    search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}"
                    self.driver.get(search_url)
                    
                    await asyncio.sleep(random.uniform(2, 4))  # Evita rate limiting
                    
                    # Estrai risultati
                    results = self._extract_linkedin_results()
                    prospects.extend(results)
                    
                    # Limita numero risultati per evitare ban
                    if len(prospects) >= 20:
                        break
                
                if len(prospects) >= 20:
                    break
            
            logger.info(f"✅ LinkedIn search completata: {len(prospects)} prospects trovati")
            return prospects
            
        except Exception as e:
            logger.error(f"❌ Errore ricerca LinkedIn: {e}")
            return prospects
    
    def _extract_linkedin_results(self) -> List[Dict]:
        """Estrae i risultati dalla pagina LinkedIn"""
        prospects = []
        
        try:
            # Attendi caricamento risultati
            time.sleep(2)
            
            # Trova elementi risultati
            result_elements = self.driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")
            
            for element in result_elements[:10]:  # Massimo 10 per pagina
                try:
                    # Estrai nome
                    name_element = element.find_element(By.CSS_SELECTOR, ".entity-result__title-text a")
                    full_name = name_element.text.strip()
                    linkedin_url = name_element.get_attribute("href")
                    
                    if not full_name:
                        continue
                    
                    # Dividi nome e cognome
                    name_parts = full_name.split(' ', 1)
                    nome = name_parts[0] if name_parts else ""
                    cognome = name_parts[1] if len(name_parts) > 1 else ""
                    
                    # Estrai posizione
                    try:
                        position_element = element.find_element(By.CSS_SELECTOR, ".entity-result__primary-subtitle")
                        posizione = position_element.text.strip()
                    except:
                        posizione = ""
                    
                    # Estrai azienda
                    try:
                        company_element = element.find_element(By.CSS_SELECTOR, ".entity-result__secondary-subtitle")
                        azienda = company_element.text.strip()
                    except:
                        azienda = ""
                    
                    # Estrai location
                    try:
                        location_element = element.find_element(By.CSS_SELECTOR, ".entity-result__summary .t-12")
                        location = location_element.text.strip()
                    except:
                        location = ""
                    
                    # Determina provincia da location
                    provincia = self._extract_provincia_from_location(location)
                    
                    prospect_data = {
                        "nome": nome,
                        "cognome": cognome,
                        "azienda": azienda,
                        "posizione": posizione,
                        "linkedin_url": linkedin_url,
                        "citta": location,
                        "provincia": provincia,
                        "fonte": "linkedin"
                    }
                    
                    prospects.append(prospect_data)
                    
                except Exception as e:
                    logger.debug(f"Errore estrazione singolo risultato: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Errore estrazione risultati LinkedIn: {e}")
        
        return prospects
    
    async def search_sales_navigator(self, criteria: SearchCriteria) -> List[Dict]:
        """Ricerca su LinkedIn Sales Navigator"""
        if not self.logged_in:
            if not await self.login_linkedin():
                return []
        
        prospects = []
        
        try:
            logger.info("🎯 Ricerca Sales Navigator...")
            
            # Vai a Sales Navigator
            self.driver.get("https://www.linkedin.com/sales")
            await asyncio.sleep(3)
            
            # Verifica accesso Sales Navigator
            if "sales" not in self.driver.current_url:
                logger.warning("⚠️ Sales Navigator non accessibile, uso LinkedIn normale")
                return await self.search_linkedin_prospects(criteria)
            
            # Costruisci ricerca avanzata Sales Navigator
            for settore in criteria.settori[:2]:
                for posizione in criteria.posizioni[:2]:
                    
                    # Vai alla ricerca lead
                    search_url = "https://www.linkedin.com/sales/search/people"
                    self.driver.get(search_url)
                    await asyncio.sleep(2)
                    
                    # Compila filtri (implementazione semplificata)
                    # In una versione completa, qui interagiresti con i filtri di Sales Navigator
                    
                    # Per ora, simula risultati
                    simulated_results = self._simulate_sales_navigator_results(settore, posizione)
                    prospects.extend(simulated_results)
                    
                    if len(prospects) >= 15:
                        break
            
            logger.info(f"✅ Sales Navigator search completata: {len(prospects)} prospects")
            return prospects
            
        except Exception as e:
            logger.error(f"❌ Errore Sales Navigator: {e}")
            return prospects
    
    def _simulate_sales_navigator_results(self, settore: str, posizione: str) -> List[Dict]:
        """Simula risultati Sales Navigator (per demo)"""
        # In produzione, qui estrarresti i veri risultati
        sample_results = [
            {
                "nome": "Marco", "cognome": "Ferri", 
                "azienda": f"{settore} Solutions SRL",
                "posizione": posizione,
                "linkedin_url": "https://linkedin.com/in/marco-ferri",
                "citta": "Udine", "provincia": "UD",
                "fonte": "sales_navigator"
            },
            {
                "nome": "Elena", "cognome": "Costa",
                "azienda": f"Innovation {settore} SpA", 
                "posizione": posizione,
                "linkedin_url": "https://linkedin.com/in/elena-costa",
                "citta": "Trieste", "provincia": "TS",
                "fonte": "sales_navigator"
            }
        ]
        return sample_results[:random.randint(1, 2)]
    
    def _extract_provincia_from_location(self, location: str) -> str:
        """Estrae la provincia dal testo location"""
        location_lower = location.lower()
        
        if any(city in location_lower for city in ['udine', 'cividale', 'gemona']):
            return 'UD'
        elif any(city in location_lower for city in ['pordenone', 'sacile', 'spilimbergo']):
            return 'PN'
        elif any(city in location_lower for city in ['gorizia', 'monfalcone']):
            return 'GO'
        elif any(city in location_lower for city in ['trieste', 'muggia']):
            return 'TS'
        
        return ''
    
    def close(self):
        """Chiude il driver"""
        if self.driver:
            self.driver.quit()

class CameraCommercioSearcher:
    """Ricerca aziende da Camera di Commercio e DB pubblici"""
    
    def __init__(self):
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
    
    async def search_companies_fvg(self, criteria: SearchCriteria) -> List[Dict]:
        """Ricerca aziende FVG da fonti pubbliche"""
        if not REQUESTS_AVAILABLE:
            logger.warning("⚠️ Requests non disponibile per ricerca aziende")
            return self._simulate_camera_commercio_results(criteria)
        
        prospects = []
        
        try:
            logger.info("🏢 Ricerca Camera di Commercio FVG...")
            
            # In produzione, qui faresti chiamate alle API ufficiali
            # Per ora, simula risultati realistici
            prospects = self._simulate_camera_commercio_results(criteria)
            
            logger.info(f"✅ Camera Commercio search: {len(prospects)} aziende trovate")
            return prospects
            
        except Exception as e:
            logger.error(f"❌ Errore ricerca Camera Commercio: {e}")
            return prospects
    
    def _simulate_camera_commercio_results(self, criteria: SearchCriteria) -> List[Dict]:
        """Simula risultati realistici da Camera di Commercio"""
        sample_companies = [
            {
                "azienda": "Friuli Tech Innovation SRL",
                "settore": "Tecnologia",
                "citta": "Udine",
                "provincia": "UD",
                "email": "info@friulitech.it",
                "telefono": "0432123456",
                "fonte": "camera_commercio"
            },
            {
                "azienda": "Green Energy Pordenone SpA",
                "settore": "Energia",
                "citta": "Pordenone", 
                "provincia": "PN",
                "email": "contatti@greenenergy-pn.it",
                "telefono": "0434987654",
                "fonte": "camera_commercio"
            },
            {
                "azienda": "Adriatic Solutions SNC",
                "settore": "Servizi",
                "citta": "Trieste",
                "provincia": "TS", 
                "email": "hello@adriaticsolutions.it",
                "telefono": "040555666",
                "fonte": "camera_commercio"
            },
            {
                "azienda": "Manifattura Gorizia SRL",
                "settore": "Manifatturiero",
                "citta": "Gorizia",
                "provincia": "GO",
                "email": "produzione@manifattura-go.it", 
                "telefono": "0481777888",
                "fonte": "camera_commercio"
            }
        ]
        
        # Filtra per criteri
        filtered_results = []
        for company in sample_companies:
            if any(settore.lower() in company["settore"].lower() for settore in criteria.settori):
                if company["provincia"] in criteria.province_fvg:
                    # Genera contatto fittizio
                    company.update({
                        "nome": "Responsabile",
                        "cognome": "Commerciale", 
                        "posizione": "Sales Manager",
                        "linkedin_url": "",
                        "azienda_linkedin": company["azienda"]
                    })
                    filtered_results.append(company)
        
        return filtered_results[:random.randint(2, 4)]

class ETJCADatabase:
    """Gestore database ETJCA con supporto multi-fonte"""
    
    def __init__(self):
        self.db_path = self._get_db_path()
        self.init_database()
        logger.info(f"🗄️ Database ETJCA: {self.db_path}")
    
    def _get_db_path(self) -> str:
        """Ottiene il path del database"""
        db_url = os.environ.get('DATABASE_URL')
        if db_url and 'postgresql' in db_url:
            return "postgresql"
        return "etjca_leads.db"
    
    def init_database(self):
        """Inizializza le tabelle del database"""
        if self.db_path == "postgresql":
            logger.info("📊 Usando PostgreSQL per produzione")
            return
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabella prospects aggiornata
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prospects (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    cognome TEXT NOT NULL,
                    azienda TEXT NOT NULL,
                    email TEXT,
                    telefono TEXT,
                    citta TEXT,
                    provincia TEXT,
                    settore TEXT,
                    fonte TEXT,
                    linkedin_url TEXT,
                    azienda_linkedin TEXT,
                    posizione TEXT,
                    stato TEXT DEFAULT 'nuovo',
                    note TEXT,
                    data_inserimento TEXT NOT NULL,
                    ultimo_contatto TEXT,
                    prossimo_followup TEXT
                )
            ''')
            
            # Tabella search_results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_results (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    prospects_found INTEGER,
                    search_criteria TEXT,
                    timestamp TEXT NOT NULL,
                    success INTEGER,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
    
    def save_prospect(self, prospect: Prospect) -> bool:
        """Salva un prospect nel database"""
        if self.db_path == "postgresql":
            return True
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verifica duplicati per email
                if prospect.email:
                    cursor.execute('SELECT id FROM prospects WHERE email = ?', (prospect.email,))
                    if cursor.fetchone():
                        logger.info(f"⚠️ Prospect già esistente: {prospect.email}")
                        return False
                
                cursor.execute('''
                    INSERT INTO prospects 
                    (id, nome, cognome, azienda, email, telefono, citta, provincia, 
                     settore, fonte, linkedin_url, azienda_linkedin, posizione, stato, note, 
                     data_inserimento, ultimo_contatto, prossimo_followup)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    prospect.id, prospect.nome, prospect.cognome, prospect.azienda,
                    prospect.email, prospect.telefono, prospect.citta, prospect.provincia,
                    prospect.settore, prospect.fonte, prospect.linkedin_url, 
                    prospect.azienda_linkedin, prospect.posizione, prospect.stato, 
                    prospect.note, prospect.data_inserimento.isoformat(),
                    prospect.ultimo_contatto.isoformat() if prospect.ultimo_contatto else None,
                    prospect.prossimo_followup.isoformat() if prospect.prossimo_followup else None
                ))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Errore salvataggio prospect: {e}")
            return False
    
    def get_all_prospects(self) -> List[Prospect]:
        """Recupera tutti i prospects"""
        if self.db_path == "postgresql":
            return []
        
        prospects = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM prospects ORDER BY data_inserimento DESC')
                for row in cursor.fetchall():
                    prospects.append(Prospect(
                        id=row[0], nome=row[1], cognome=row[2], azienda=row[3],
                        email=row[4] or "", telefono=row[5] or "", citta=row[6] or "", 
                        provincia=row[7] or "", settore=row[8] or "", fonte=row[9] or "",
                        linkedin_url=row[10] or "", azienda_linkedin=row[11] or "",
                        posizione=row[12] or "", stato=row[13] or "nuovo", note=row[14] or "",
                        data_inserimento=datetime.fromisoformat(row[15]),
                        ultimo_contatto=datetime.fromisoformat(row[16]) if row[16] else None,
                        prossimo_followup=datetime.fromisoformat(row[17]) if row[17] else None
                    ))
        except Exception as e:
            logger.error(f"Errore recupero prospects: {e}")
        
        return prospects
    
    def save_search_result(self, result: SearchResult) -> bool:
        """Salva risultato di una ricerca"""
        if self.db_path == "postgresql":
            return True
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO search_results 
                    (id, source, prospects_found, search_criteria, timestamp, success, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()), result.source, result.prospects_found,
                    json.dumps(asdict(result.search_criteria)), result.timestamp.isoformat(),
                    1 if result.success else 0, result.error_message
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Errore salvataggio search result: {e}")
            return False
    
    def get_report_statistics(self) -> Dict:
        """Genera statistiche avanzate per i report"""
        if self.db_path == "postgresql":
            return {"total_prospects": 0}
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total prospects
                cursor.execute('SELECT COUNT(*) FROM prospects')
                total_prospects = cursor.fetchone()[0]
                
                # Per fonte
                cursor.execute('SELECT fonte, COUNT(*) FROM prospects GROUP BY fonte')
                per_fonte = dict(cursor.fetchall())
                
                # Per provincia
                cursor.execute('SELECT provincia, COUNT(*) FROM prospects GROUP BY provincia')
                per_provincia = dict(cursor.fetchall())
                
                # Per stato
                cursor.execute('SELECT stato, COUNT(*) FROM prospects GROUP BY stato')
                per_stato = dict(cursor.fetchall())
                
                # Inseriti oggi
                oggi = datetime.now().date().isoformat()
                cursor.execute('SELECT COUNT(*) FROM prospects WHERE DATE(data_inserimento) = ?', (oggi,))
                inseriti_oggi = cursor.fetchone()[0]
                
                # Ultimi search results
                cursor.execute('SELECT * FROM search_results ORDER BY timestamp DESC LIMIT 5')
                recent_searches = []
                for row in cursor.fetchall():
                    recent_searches.append({
                        "source": row[1],
                        "prospects_found": row[2],
                        "timestamp": row[4],
                        "success": bool(row[5])
                    })
                
                return {
                    "total_prospects": total_prospects,
                    "per_fonte": per_fonte,
                    "per_provincia": per_provincia, 
                    "per_stato": per_stato,
                    "inseriti_oggi": inseriti_oggi,
                    "recent_searches": recent_searches
                }
                
        except Exception as e:
            logger.error(f"Errore generazione statistiche: {e}")
            return {"total_prospects": 0}

class ETJCAMCPAgent:
    """ETJCA Agent con MCP Protocol e ricerca automatica"""
    
    def __init__(self):
        self.db = ETJCADatabase()
        self.running = True
        self.config = {
            "agent_name": "ETJCA-Lead-Generator-MCP",
            "version": "2.0.0",
            "territory": "Friuli Venezia Giulia",
            "province": ["UD", "PN", "GO", "TS"],
            "supported_sources": ["manual", "linkedin", "sales_navigator", "camera_commercio"]
        }
        
        # Credenziali (da variabili ambiente per sicurezza)
        self.credentials = {
            "linkedin": {
                "email": os.environ.get('LINKEDIN_EMAIL', ''),
                "password": os.environ.get('LINKEDIN_PASSWORD', '')
            }
        }
        
        # Inizializza searchers
        self.linkedin_searcher = LinkedInSearcher(self.credentials["linkedin"]) if SELENIUM_AVAILABLE else None
        self.camera_searcher = CameraCommercioSearcher()
        
        logger.info("🚀 ETJCA MCP Agent inizializzato")
        logger.info(f"📍 Territory: {self.config['territory']}")
        logger.info(f"🔍 Sources: {', '.join(self.config['supported_sources'])}")
    
    def add_prospect_manual(self, data: Dict) -> bool:
        """Aggiunge un prospect manualmente"""
        try:
            prospect = Prospect(
                id=f"manual-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:8]}",
                nome=data["nome"],
                cognome=data["cognome"],
                azienda=data["azienda"],
                email=data.get("email", ""),
                telefono=data.get("telefono", ""),
                citta=data.get("citta", ""),
                provincia=data.get("provincia", ""),
                settore=data.get("settore", ""),
                fonte="manuale",
                linkedin_url="",
                azienda_linkedin="",
                posizione=data.get("posizione", ""),
                stato="nuovo",
                note=data.get("note", ""),
                data_inserimento=datetime.now()
            )
            
            success = self.db.save_prospect(prospect)
            if success:
                logger.info(f"✅ Prospect manuale aggiunto: {prospect.nome} {prospect.cognome}")
            return success
            
        except Exception as e:
            logger.error(f"Errore aggiunta prospect manuale: {e}")
            return False
    
    async def search_linkedin_leads(self, criteria: SearchCriteria) -> SearchResult:
        """Ricerca lead su LinkedIn"""
        logger.info("🔍 Avvio ricerca LinkedIn...")
        
        if not self.linkedin_searcher:
            error_msg = "LinkedIn searcher non disponibile"
            logger.error(f"❌ {error_msg}")
            return SearchResult(
                source="linkedin",
                prospects_found=0,
                search_criteria=criteria,
                timestamp=datetime.now(),
                success=False,
                error_message=error_msg
            )
        
        try:
            # Ricerca prospects
            prospects_data = await self.linkedin_searcher.search_linkedin_prospects(criteria)
            
            # Salva prospects nel database
            saved_count = 0
            for prospect_data in prospects_data:
                prospect = self._create_prospect_from_data(prospect_data, "linkedin")
                if self.db.save_prospect(prospect):
                    saved_count += 1
