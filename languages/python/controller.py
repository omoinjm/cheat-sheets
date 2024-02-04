@router.post(
    "/providers",
    response_model=ResponseValidatorSingle,
)
def create_provider_handler(
    response: Response,
    provider_data: ProviderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProviderService(current_user.id)
    provider = service.create_provider(db=db, provider_data=provider_data)
    if not provider:
        raise HTTPException(status_code=500, detail="Provider creation failed")
    response.status_code = status.HTTP_201_CREATED
    return success_response_single(provider)
