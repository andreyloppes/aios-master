# Google Auth — Troubleshooting

Problemas comuns e soluções para Google OAuth com Supabase.

---

## 1. redirect_uri_mismatch

**Sintoma:** Erro "Error 400: redirect_uri_mismatch" no Google consent screen.

**Causa:** A redirect URI configurada no Google Cloud Console não bate exatamente com a que o Supabase envia.

**Solução:**
1. No Google Cloud Console, vá em Credentials > seu OAuth Client
2. Verifique que a Authorized Redirect URI é **exatamente**:
   ```
   https://<project-ref>.supabase.co/auth/v1/callback
   ```
3. Sem barra no final, sem espaços, HTTPS obrigatório
4. Aguarde ~5 minutos para propagação após salvar

---

## 2. Login redireciona para localhost

**Sintoma:** Após autenticar no Google, o usuário é redirecionado para `localhost:3000` em vez do app em produção.

**Causa:** O Site URL no Supabase Dashboard está configurado como `http://localhost:3000`.

**Solução:**
1. Supabase Dashboard > Authentication > URL Configuration
2. Altere o **Site URL** para sua URL de produção: `https://seu-app.vercel.app`
3. Adicione em **Redirect URLs**: `https://seu-app.vercel.app/auth/callback`
4. Para development, adicione também: `http://localhost:3000/auth/callback`

---

## 3. Usuário não aparece na tabela `users`

**Sintoma:** Login funciona mas a tabela `public.users` não recebe o registro.

**Causa:** Trigger `on_auth_user_created` não existe ou tem erro.

**Solução:**
Execute no SQL Editor do Supabase:
```sql
-- Verificar se o trigger existe
SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';

-- Se não existir, criar:
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, name, email, avatar_url)
  VALUES (
    NEW.id,
    COALESCE(
      NEW.raw_user_meta_data ->> 'full_name',
      NEW.raw_user_meta_data ->> 'name',
      NEW.raw_user_meta_data ->> 'user_name',
      ''
    ),
    COALESCE(NEW.email, ''),
    COALESCE(NEW.raw_user_meta_data ->> 'avatar_url', NULL)
  )
  ON CONFLICT (id) DO UPDATE SET
    name = COALESCE(EXCLUDED.name, users.name),
    email = COALESCE(EXCLUDED.email, users.email),
    avatar_url = COALESCE(EXCLUDED.avatar_url, users.avatar_url),
    updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

## 4. Nome do usuário vem vazio

**Sintoma:** Usuário logado via Google tem nome vazio no perfil.

**Causa:** O trigger usa `raw_user_meta_data ->> 'name'` mas o Google envia como `'full_name'`.

**Solução:** Atualizar o trigger para usar COALESCE com todos os campos possíveis (ver item 3 acima).

Para corrigir usuários existentes:
```sql
UPDATE public.users u
SET name = COALESCE(
  au.raw_user_meta_data ->> 'full_name',
  au.raw_user_meta_data ->> 'name',
  au.raw_user_meta_data ->> 'user_name',
  ''
)
FROM auth.users au
WHERE u.id = au.id AND (u.name IS NULL OR u.name = '');
```

---

## 5. "Email already registered" no OAuth

**Sintoma:** Usuário que já criou conta com email/senha não consegue logar com Google (mesmo email).

**Causa:** Por padrão, Supabase não faz merge de identidades.

**Solução:**
1. Supabase Dashboard > Authentication > Providers
2. Ative "Allow linking of existing accounts" (se disponível)
3. Ou instrua o usuário a logar com email/senha primeiro, depois vincular OAuth nas configurações

---

## 6. Callback falha com "auth_callback_failed"

**Sintoma:** Após autorizar no Google, volta pra login com `?error=auth_callback_failed`.

**Causas possíveis:**
1. Código de autorização expirou (>5 minutos entre consent e callback)
2. Cookies bloqueados pelo navegador
3. Supabase anon key incorreta no `.env`

**Diagnóstico:**
```javascript
// No callback route, logar o erro:
const { error } = await supabase.auth.exchangeCodeForSession(code);
console.error('Callback error:', error);
```

---

## 7. PKCE flow não funciona em produção

**Sintoma:** Funciona em localhost mas falha em produção.

**Causa:** O middleware não está refreshando os cookies corretamente.

**Solução:** Garantir que o middleware:
1. Chama `supabase.auth.getUser()` em TODAS as rotas (não pular)
2. Usa o pattern correto de `setAll` que recria a response
3. Está no matcher correto (não excluindo rotas necessárias)

---

## 8. Google OAuth app "unverified"

**Sintoma:** Tela de aviso "This app isn't verified" no Google consent.

**Causa:** App em modo de teste, não publicado.

**Solução para teste:**
- Adicione emails de teste em OAuth consent screen > Test users
- Ou publique o app quando estiver pronto para produção

**Solução para produção:**
1. Google Cloud Console > OAuth consent screen
2. Clique em "Publish App"
3. Se pedir verificação, submeta (pode levar dias)
4. Para apps internos, use "Internal" em vez de "External"

---

## Checklist de Diagnóstico Rápido

```
[ ] .env.local tem SUPABASE_URL e ANON_KEY corretos?
[ ] Google Cloud: redirect URI = https://<ref>.supabase.co/auth/v1/callback?
[ ] Supabase: Google provider habilitado com Client ID + Secret?
[ ] Supabase: Site URL = URL do app em produção?
[ ] Supabase: Redirect URLs inclui https://app.com/auth/callback?
[ ] Callback route existe em /auth/callback?
[ ] Middleware não bloqueia /auth/callback?
[ ] Trigger on_auth_user_created existe no banco?
```
