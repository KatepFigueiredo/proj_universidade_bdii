-- Grant EXECUTE na função para role_professor (e para o app_user, se necessário)
GRANT EXECUTE ON FUNCTION criar_aula_bd(TEXT, DATE, TIME, TIME, INT) TO role_professor;
GRANT EXECUTE ON FUNCTION criar_aula_bd(TEXT, DATE, TIME, TIME, INT) TO app_user;