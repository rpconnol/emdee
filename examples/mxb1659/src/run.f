program run_dStar
	use iso_fortran_env, only : output_unit, error_unit
    use NScool_def
    use NScool_lib
    use constants_def, only : boltzmann
    use argparse
    
    character(len=*), parameter :: default_dStar_dir = '../../dStar'
    character(len=*), parameter :: default_inlist_file = 'inlist'
    character(len=64) :: my_dStar_dir
    character(len=64) :: inlist
    real(dp) :: eV_to_MK
    type(NScool_info), pointer :: s=>null()
    integer :: ierr, NScool_id, i
    real(dp), dimension(7) :: pred_Teff, obs_Teff, obs_Teff_sig
    real(dp) :: chi2
    
    ierr = 0
    call command_arg_set( &
        & 'dStar_directory',"sets the main dStar root directory",ierr, &
        & flag='D',takes_parameter=.TRUE.)
    call check_okay('set command argument dStar_directory',ierr)
    
    call command_arg_set( &
        & 'inlist_file','sets the namelist parameter file',ierr, &
        & flag='I',takes_parameter=.TRUE.)
    call check_okay('set command argument inlist file',ierr)
    
    call parse_arguments(ierr)
    call check_okay('parse_arguments',ierr)

    my_dStar_dir = trim(get_command_arg('dStar_directory'))
    if (len_trim(my_dStar_dir)==0) my_dStar_dir = default_dStar_dir
    inlist = trim(get_command_arg('inlist_file'))
    if (len_trim(inlist)==0) inlist = default_inlist_file
 
    call NScool_init(my_dStar_dir, ierr)
    call check_okay('NScool_init',ierr)
    
    NScool_id = alloc_NScool(ierr)
    call check_okay('NScool_id',ierr)
    
    call NScool_setup(NScool_id,inlist,ierr)
    call check_okay('NScool_setup',ierr)
    
    call get_NScool_info_ptr(NScool_id,s,ierr)
    call check_okay('get_NScool_info_ptr',ierr)

    call NScool_create_model(NScool_id,ierr)
    call check_okay('NScool_create_model',ierr)

    call NScool_evolve_model(NScool_id,ierr)        
    call check_okay('NScool_evolve_model',ierr)
   
   
   	! Much of the following functionality is cannabalized from an example shipped with 
   	! dStar. 
   	! The intervals that are set up with epoch_boundaries in the inlist preamble
   	! match the times of the xray observations, and the Teff at those times become
   	! Teff_monitor. chi2 is calculated by comparing Teff_monitor to the observation
   	! temperatures and error bars.
   
    ! we don't want to compare the effective temp. at t = 0, the end of the 
    ! outburst, so clip the first Teff_monitor from our comparison
    pred_Teff = s% Teff_monitor(2:)/1.0e6
    eV_to_MK = 1.602176565e-12_dp/boltzmann/1.0e6
    
    ! observed effective temperatures (eV) and uncertainties WITH the 2013 upper limit
    !obs_Teff = [121.0,85.0,77.0,73.0,58.0,54.0,56.0,49.0] * eV_to_MK
    !obs_Teff_sig = [1.0,1.0,1.0,1.0,2.0,3.0,2.0,2.0] * eV_to_MK
    
    ! observed Teff and uncertainties WITHOUT the final (2013) observation
    obs_Teff = [121.0,85.0,77.0,73.0,58.0,54.0,56.0] * eV_to_MK
    obs_Teff_sig = [1.0,1.0,1.0,1.0,2.0,3.0,2.0] * eV_to_MK
    
    ! Calculate chi2
    chi2 = sum((pred_Teff-obs_Teff)**2 / obs_Teff_sig**2 )
    
    !  We suppress this detailed output for now, emdee only wants chi2
    !write(output_unit,*)
    !write(output_unit,'(a7,a6,tr3,a12)') 'time','Teff','obs. range'
    !write(output_unit,'(a7,a6,tr3,a12)') '[d]','[MK]','[MK]'
    !write(output_unit,'(13("-"),tr3,12("-"))')
    !do i = 1, 8
    !    write(output_unit,'(f7.1,f6.3,tr3,f6.3,f6.3)')  &
    !    & s% t_monitor(i+1), &
    !    & pred_Teff(i),(obs_Teff(i)-obs_Teff_sig(i)), &
    !    & (obs_Teff(i)+obs_Teff_sig(i))
    !end do
    !write(output_unit,*)
    !write(output_unit,'(a,f6.2)') 'chi2 = ',chi2
    
    ! emdee ONLY wants chi2 at the end, by itself, on a new line. This should be the 
    ! final stdout output from the dStar execution.
    write(output_unit,'(a)') 'chi2 = '
    write(output_unit,'(f16.2)') chi2
    
    call NScool_shutdown
    
contains
	subroutine check_okay(msg,ierr)
		character(len=*), intent(in) :: msg
		integer, intent(inout) :: ierr
		if (ierr /= 0) then
			write (error_unit,*) trim(msg)//': ierr = ',ierr
			if (ierr < 0) stop
		end if
	end subroutine check_okay
end program run_dStar
